import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SearchPage from './pages/SearchPage/SearchPage';
import ResultMap from "./components/Map";

function App() {
  return (
    <BrowserRouter>
      <Routes>
          <Route path="/result" element={<ResultMap />}></Route>
          <Route path="/" element={<SearchPage />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
