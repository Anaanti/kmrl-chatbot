export interface Message {
  id: string
  type: "user" | "bot"
  content: string
  timestamp: Date
}

export interface Source {
  document: string
  score: number
}
