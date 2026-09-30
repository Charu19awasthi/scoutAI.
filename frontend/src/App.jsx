import { useState } from "react";

function App() {
  const [status, setStatus] = useState("Not checked");
  const [loading, setLoading] = useState(false);

  const checkBackend = async () => {
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/health");

      if (!response.ok) {
        throw new Error("Backend unavailable");
      }

      const data = await response.json();

      if (data.status === "healthy") {
        setStatus("Connected");
      } else {
        setStatus("Offline");
      }
    } catch (error) {
      setStatus("Offline");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#05070b] text-white">
      <nav className="border-b border-white/10 bg-[#080b12]/80">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-bold tracking-tight">
              Scout<span className="text-cyan-400">AI</span>
            </h1>
            <p className="text-xs text-gray-500">
              Research Intelligence
            </p>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2">
            <span
              className={`h-2 w-2 rounded-full ${
                status === "Connected"
                  ? "bg-green-400"
                  : "bg-gray-500"
              }`}
            />

            <span className="text-sm text-gray-300">
              Backend {status}
            </span>
          </div>
        </div>
      </nav>

      <main className="mx-auto flex min-h-[calc(100vh-80px)] max-w-5xl flex-col items-center justify-center px-6 py-16 text-center">
        <div className="mb-6 rounded-full border border-cyan-400/20 bg-cyan-400/5 px-4 py-2 text-sm text-cyan-300">
          Evidence-First AI Research Platform
        </div>

        <h2 className="max-w-4xl text-5xl font-bold leading-tight tracking-tight md:text-6xl">
          Ask a business question.
          <br />
          <span className="text-cyan-400">
            Get a verified dataset.
          </span>
        </h2>

        <p className="mt-6 max-w-2xl text-lg leading-8 text-gray-400">
          ScoutAI transforms natural-language research requirements
          into structured, evidence-backed datasets.
        </p>

        <div className="mt-10 flex flex-wrap justify-center gap-4">
          <button
            onClick={checkBackend}
            disabled={loading}
            className="rounded-lg bg-cyan-400 px-6 py-3 font-semibold text-black transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Checking..." : "Check Backend"}
          </button>

          <button className="rounded-lg border border-white/10 bg-white/5 px-6 py-3 font-semibold text-white transition hover:bg-white/10">
            New Research
          </button>
        </div>

        <div className="mt-16 grid w-full gap-4 md:grid-cols-3">
          <FeatureCard
            title="Research Planning"
            description="Convert natural-language requirements into structured research workflows."
          />

          <FeatureCard
            title="Evidence-First"
            description="Trace every result back to its source and supporting evidence."
          />

          <FeatureCard
            title="Structured Data"
            description="Clean, validate, deduplicate and export research results."
          />
        </div>
      </main>
    </div>
  );
}

function FeatureCard({ title, description }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 text-left transition hover:border-cyan-400/30 hover:bg-white/[0.05]">
      <h3 className="text-lg font-semibold">{title}</h3>

      <p className="mt-3 text-sm leading-6 text-gray-400">
        {description}
      </p>
    </div>
  );
}

export default App;