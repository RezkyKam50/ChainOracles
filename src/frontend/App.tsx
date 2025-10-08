import { useState } from "react";

function App() {
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  const handleGreet = async () => {
    const response = await fetch(`http://localhost:8000/greet?name=${name}`);
    const data = await response.json();
    setMessage(data.message);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-4">Greeting App</h1>

      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter your name"
        className="border p-2 rounded w-64"
      />

      <button
        onClick={handleGreet}
        className="mt-3 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Greet Me
      </button>

      {message && <p className="mt-4 text-lg">{message}</p>}
    </div>
  );
}

export default App;
