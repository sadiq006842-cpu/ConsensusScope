"use client"

import {
  Shield,
  LayoutDashboard,
  Brain,
  Activity,
  BarChart3,
  Settings
} from "lucide-react"

export default function Sidebar() {

  const menu = [
    {
      name: "Dashboard",
      icon: LayoutDashboard
    },
    {
      name: "Consensus AI",
      icon: Brain
    },
    {
      name: "Validators",
      icon: Shield
    },
    {
      name: "Analytics",
      icon: BarChart3
    },
    {
      name: "Activity",
      icon: Activity
    },
    {
      name: "Settings",
      icon: Settings
    }
  ]

  return (

    <aside
      className="
        h-screen
        w-[260px]
        fixed
        left-0
        top-0
        border-r
        border-white/10
        bg-black/40
        backdrop-blur-2xl
        p-6
        hidden
        lg:flex
        flex-col
      "
    >

      <div className="mb-10">

        <h1
          className="
            text-3xl
            font-black
            tracking-tight
          "
        >
          ConsensusScope
        </h1>

        <p className="text-zinc-500 mt-2">
          AI Governance Platform
        </p>

      </div>

      <div className="space-y-3">

        {menu.map((item, index) => {

          const Icon = item.icon

          return (

            <button
              key={index}
              className="
                w-full
                flex
                items-center
                gap-4
                px-4
                py-3
                rounded-2xl
                text-zinc-300
                hover:bg-white/10
                hover:text-white
                transition-all
              "
            >

              <Icon size={20} />

              <span className="font-medium">
                {item.name}
              </span>

            </button>

          )
        })}

      </div>

      <div
        className="
          mt-auto
          border
          border-blue-500/20
          bg-blue-500/10
          rounded-2xl
          p-4
        "
      >

        <p className="text-sm text-zinc-300">
          Network Status
        </p>

        <h3 className="text-xl font-bold mt-2">
          ACTIVE
        </h3>

        <div className="flex gap-2 mt-3">

          <div
            className="
              w-3
              h-3
              rounded-full
              bg-green-500
              animate-pulse
            "
          />

          <span className="text-sm text-zinc-400">
            Validators Online
          </span>

        </div>

      </div>

    </aside>
  )
}