"use client"

import type React from "react"

import type { Message } from "@/lib/types"

interface ChatWindowProps {
  messages: Message[]
  messagesEndRef: React.RefObject<HTMLDivElement>
}

export default function ChatWindow({ messages, messagesEndRef }: ChatWindowProps) {
  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-slate-50 to-white">
      {messages.map((message) => (
        <div key={message.id} className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
          <div
            className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
              message.type === "user"
                ? "bg-blue-500 text-white rounded-br-none"
                : "bg-green-100 text-slate-900 rounded-bl-none border border-green-200"
            }`}
          >
            <p className="text-sm leading-relaxed">{message.content}</p>
            <span className="text-xs opacity-70 mt-1 block">
              {message.timestamp.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </span>
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  )
}
