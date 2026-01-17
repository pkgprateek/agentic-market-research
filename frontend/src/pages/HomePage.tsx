export default function HomePage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="flex flex-col items-center justify-center min-h-[80vh] space-y-6">
        <h1 className="text-4xl font-bold tracking-tight">
          <span className="mdi mdi-magnify mr-2"></span>
          Agentic Market Research
        </h1>
        <p className="text-xl text-muted-foreground text-center max-w-2xl">
          Enterprise-grade AI-powered competitive intelligence.
          80x faster, 2000x cheaper than manual research.
        </p>
        <div className="flex gap-4 mt-8">
          <button className="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 text-sm font-medium text-primary-foreground shadow hover:bg-primary/90">
            <span className="mdi mdi-play mr-2"></span>
            Start Research
          </button>
        </div>
      </div>
    </main>
  )
}
