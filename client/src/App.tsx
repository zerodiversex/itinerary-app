import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SearchPage from './pages/SearchPage/SearchPage';
import MapPage from "./pages/MapPage/MapPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/result" element={<MapPage />}></Route>
        <Route path="/" element={<SearchPage />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
