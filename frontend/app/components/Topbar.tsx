"use client";

import { useEffect, useState } from "react";

declare global {
  interface Window {
    ethereum?: {
      request: (args: { method: string }) => Promise<string[]>;
    };
  }
}

interface TopbarProps {
  title: string;
}

export default function Topbar({ title }: TopbarProps) {
  const [mounted, setMounted] = useState(false);
  const [hasMetaMask, setHasMetaMask] = useState(false);
  const [account, setAccount] = useState<string | null>(null);
  const [connecting, setConnecting] = useState(false);

  useEffect(() => {
    queueMicrotask(() => {
      setMounted(true);
      setHasMetaMask(
        typeof window !== "undefined" && typeof window.ethereum !== "undefined",
      );
    });
  }, []);

  const connectWallet = async () => {
    if (!window.ethereum) {
      return;
    }

    setConnecting(true);

    try {
      const accounts = await window.ethereum.request({
        method: "eth_requestAccounts",
      });
      setAccount(accounts[0] ?? null);
    } catch {
      // User rejected the request.
    } finally {
      setConnecting(false);
    }
  };

  const truncate = (addr: string) => `${addr.slice(0, 6)}...${addr.slice(-4)}`;

  return (
    <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/80 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between px-5 lg:px-8">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-violet-600">
            Optimistic Democracy Engine
          </p>
          <h1 className="text-xl font-bold text-slate-950">{title}</h1>
        </div>

        {!mounted ? null : account ? (
          <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-2 font-mono text-sm text-slate-900">
            <span className="h-2 w-2 rounded-full bg-emerald-300" />
            {truncate(account)}
          </div>
        ) : hasMetaMask ? (
          <button
            type="button"
            onClick={connectWallet}
            disabled={connecting}
            className="inline-flex items-center gap-2 rounded-full bg-violet-500 px-4 py-2.5 text-sm font-medium text-white hover:bg-violet-400 disabled:opacity-60"
          >
            {connecting ? "Connecting..." : "Connect Wallet"}
          </button>
        ) : (
          <a
            href="https://metamask.io"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 rounded-full bg-violet-500 px-4 py-2.5 text-sm font-medium text-white hover:bg-violet-400"
          >
            Install MetaMask
          </a>
        )}
      </div>
    </header>
  );
}
