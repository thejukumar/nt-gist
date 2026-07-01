import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Support Context Budget Lab",
  description:
    "UI-first A/B benchmark comparing full-history vs pruning-aware Nebius + Tavily support agents.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
