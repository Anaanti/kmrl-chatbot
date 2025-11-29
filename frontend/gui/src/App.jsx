import { useState, useRef, useEffect } from "react"
// Assuming these component imports are correct based on your folder structure
import ChatWindow from "./components/chat-window"
import ChatInput from "./components/chat-input"
import SourcesList from "./components/sources-list"

// --- Constants ---
const API_URL = "http://127.0.0.1:8000/api/ask/"

// Function to handle the actual API communication (Mock is removed)
async function fetchRAGResponse(query) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: query }),
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`Django API Error: ${response.status} - ${errorText.substring(0, 50)}...`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error("fetchRAGResponse error:", error)
    throw error
  }
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      id: "1",
      type: "bot",
      content: "Hello! I'm the KMRL Knowledge Transfer Chatbot. How can I help you today?",
      timestamp: new Date(),
    },
  ])
  // State is now pure JavaScript array/object
  const [sources, setSources] = useState([]) 
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (text) => {
    if (!text.trim()) return

    // 1. Define and add user message synchronously
    const userMessage = {
      id: Date.now().toString(),
      type: "user",
      content: text,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)
    
    // NOTE: Timeout logic removed here. The system will now wait indefinitely.

    try {
      // API CALL: This will now wait for the full CPU processing time (minutes)
      const result = await fetchRAGResponse(text)

      // --- CRITICAL ANSWER CLEANING ---
      const fullAnswer = result.answer
      // Use regex to remove known artifacts and repetition for clean display
      const cleanAnswer = fullAnswer.replace(/(Answer:.*|^-eslint-disable-next-line.*)/s, '').trim() || 
                           "I cannot retrieve a clean answer from the model.";

      // Add bot response
      const botMessage = {
        id: (Date.now() + 1).toString(),
        type: "bot",
        content: cleanAnswer,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
      
      // Update sources with the raw Django output
      setSources(result.sources || []) 
      
    } catch (error) {
      console.error("Error sending query:", error)
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        type: "bot",
        content: `Sorry, there was an error processing your request: ${error.message}`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
      
    } finally {
      // This will only run after the API call fully succeeds OR fully fails (crashes).
      setIsLoading(false)
    }
  }
  
  // The SourcesList expects { document: string, score: number, content: string } structure.
  // We map the raw Django output to this format for the child component.
  const mappedSources = sources.map(source => ({
    document: source.doc_name,
    score: source.similarity,
    content: source.content
  }))
  
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">KMRL Knowledge Transfer Chatbot</h1>
          <p className="text-slate-600">Ask questions and get answers from our knowledge base</p>
        </div>

        {/* Chat Window */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden flex flex-col h-96 mb-4">
          <ChatWindow messages={messages} messagesEndRef={messagesEndRef} />
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-lg p-4 mb-4">
          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>

        {/* Sources Section */}
        {mappedSources.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-4">
            {/* Pass the mapped sources to the SourcesList component */}
            <SourcesList sources={mappedSources} /> 
          </div>
        )}
      </div>
    </main>
  )
}