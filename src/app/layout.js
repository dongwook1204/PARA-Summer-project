import "./globals.css";

export const metadata = {
  title: "ReloadK",
  description: "AI Review Optimizer",
  themeColor: "#ffffff",
};

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <body className="min-h-screen bg-gradient-to-br from-white via-brand-50 to-white text-gray-800">
        {children}
      </body>
    </html>
  );
}
