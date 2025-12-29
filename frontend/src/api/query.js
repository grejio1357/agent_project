// src/api/query.js

export async function queryBackend(question) {
  const response = await fetch("http://localhost:8000/api/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("Backend request failed");
  }

  return response.json();
}
