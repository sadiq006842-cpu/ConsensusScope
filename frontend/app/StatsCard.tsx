interface Props {
  title: string
  value: string
}

export default function StatsCard({
  title,
  value
}: Props) {

  return (

    <div
      className="
        bg-white/5
        border
        border-white/10
        rounded-3xl
        p-6
      "
    >

      <p className="text-zinc-500">
        {title}
      </p>

      <h2
        className="
          text-4xl
          font-black
          mt-3
        "
      >
        {value}
      </h2>

    </div>
  )
}