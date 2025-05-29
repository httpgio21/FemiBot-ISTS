import './global.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home/Home'
import Integrantes from './pages/Integrantes/Integrantes'
import ChatBot from './pages/ChatBot/ChatBot'

function App() {
  

  return (
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/integrantes" element={<Integrantes />} />
          <Route path="/chatbotIST" element={<ChatBot/>} />
        </Routes>
      </Router>
      
  )
}

export default App
