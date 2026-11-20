import { Navigate, Route, BrowserRouter as Router, Routes } from "react-router-dom"

import { AppLayout } from "@/components/layout/AppLayout"
import { AppInitializer } from "@/components/loader/AppInitializer"
import { DashboardPage } from "@/pages/DashboardPage"
import { DataQualityPage } from "@/pages/DataQualityPage"
import { DischargePage } from "@/pages/DischargePage"
import { InbornPage } from "@/pages/InbornPage"
import { OutbornPage } from "@/pages/OutbornPage"

function App() {
  return (
    <AppInitializer>
      <Router>
        <Routes>
          <Route element={<AppLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="inborn" element={<InbornPage />} />
            <Route path="outborn" element={<OutbornPage />} />
            <Route path="discharge" element={<DischargePage />} />
            <Route path="data-quality" element={<DataQualityPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </Router>
    </AppInitializer>
  )
}

export default App
