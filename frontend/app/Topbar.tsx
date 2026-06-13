"use client"

import {
  Bell,
  Search
} from "lucide-react"

export default function Topbar() {

  return (

    <div
      className="
        flex
        items-center
        justify-between
        mb-8
      "
    >

      <div>

        <h1
          className="
            text-4xl
            font-black
          "
        >
          Dashboard
        </h1>

        <p className="text-zinc-500 mt-2">
          AI governance monitoring
        </p>

      </div>

      <div className="flex items-center gap-4">

        <div
          className="
            flex
            items-center
            gap-3
            bg-white/5
            border
            border-white/10
            rounded-2xl
            px-4
            py-3
          "
        >

          <Search size={18} />

          <input
            placeholder="Search..."
            className="
              bg-transparent
              outline-none
              text-sm
            "
          />

        </div>

        <button
          className="
            p-3
            rounded-2xl
            bg-white/5
            border
            border-white/10
          "
        >

          <Bell size={20} />

        </button>

      </div>

    </div>
  )
}