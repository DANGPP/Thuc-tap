import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DetailEventPage from "./pages/DetailEventPage";
import EventPage from "./pages/EventPage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import PrivateRoute from "./components/PrivateRoute"; // ✅ Thêm dòng này

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* ✅ Các route cần đăng nhập */}
        <Route
          path="/events"
          element={
            <PrivateRoute>
              <EventPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/events/:eventid"
          element={
            <PrivateRoute>
              <DetailEventPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
