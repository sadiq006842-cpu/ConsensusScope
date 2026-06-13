import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://consensusscope.ai"),
  title: {
    default: "ConsensusScope | GenLayer Governance Intelligence",
    template: "%s | ConsensusScope",
  },
  description:
    "ConsensusScope is a GenLayer Governance Intelligence Layer for AI validator swarms, Optimistic Democracy simulation, risk analysis, and consensus observability.",
  keywords: [
    "ConsensusScope",
    "GenLayer Governance Intelligence",
    "AI Validator Swarm",
    "Optimistic Democracy Engine",
    "Governance Intelligence Layer",
    "AI governance",
    "validator simulation",
  ],
  applicationName: "ConsensusScope",
  authors: [{ name: "ConsensusScope" }],
  creator: "ConsensusScope",
  publisher: "ConsensusScope",
  icons: {
    icon: "/favicon.ico",
  },
  openGraph: {
    title: "ConsensusScope | GenLayer Governance Intelligence",
    description:
      "AI-native governance command center for validator intelligence, weighted consensus, disagreement analysis, and risk simulation.",
    siteName: "ConsensusScope",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "ConsensusScope | GenLayer Governance Intelligence",
    description: "Governance Intelligence Layer for AI Validator Swarms and Optimistic Democracy.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
