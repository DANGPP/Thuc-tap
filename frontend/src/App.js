import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DetailEventPage from "./pages/DetailEventPage";
import EventPage from "./pages/EventPage";

function App() {
  return (
    <Router>
    <Routes>
      <Route path="/events" element={<EventPage />} />
      <Route path="/events/:eventid" element={<DetailEventPage />}/>
    </Routes>
  </Router>
  );
}

export default App;
