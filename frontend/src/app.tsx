import { BrowserRouter, Routes, Route } from "react-router-dom";

const App = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<div></div>} index />
                <Route path="/" element={<div></div>} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;