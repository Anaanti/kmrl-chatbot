"use client"

import { useState, useRef, useEffect } from "react"
import ChatWindow from "@/components/chat-window"
import ChatInput from "@/components/chat-input"
import SourcesList from "@/components/sources-list"
import type { Message, Source } from "@/lib/types"

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "bot",
      content: "Hello! I'm the KMRL Knowledge Transfer Chatbot. How can I help you today?",
      timestamp: new Date(),
    },
  ])
  const [sources, setSources] = useState<Source[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: text,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    // Call sendQuery function
    try {
      const result = await sendQuery(text)

      // Add bot response
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "bot",
        content: result.response,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
      setSources(result.sources || [])
    } catch (error) {
      console.error("Error sending query:", error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "bot",
        content: "Sorry, there was an error processing your request. Please try again.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

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
        {sources.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-4">
            <SourcesList sources={sources} />
          </div>
        )}
      </div>
    </main>
  )
}

// Main sendQuery function that communicates with the API
async function sendQuery(query: string) {
  try {
    const response = await fetch("/api/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    })

    if (!response.ok) {
      throw new Error("API request failed")
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error("sendQuery error:", error)
    throw error
  }
}
