import { Navigate, Route, BrowserRouter as Router, Routes } from "react-router-dom"

import { AppLayout } from "@/components/layout/AppLayout"
import { DashboardPage } from "@/pages/DashboardPage"
import { DischargePage } from "@/pages/DischargePage"
import { InbornPage } from "@/pages/InbornPage"
import { OutbornPage } from "@/pages/OutbornPage"

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="inborn" element={<InbornPage />} />
          <Route path="outborn" element={<OutbornPage />} />
          <Route path="discharge" element={<DischargePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
