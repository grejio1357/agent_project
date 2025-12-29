import { useState } from "react";
import { queryBackend } from "./api/query";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await queryBackend(question);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", fontFamily: "Arial" }}>
      <h1>🌱 Agri AI Assistant</h1>

      {/* 질문 입력 */}
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        rows={3}
        style={{ width: "100%", padding: 10, fontSize: 16 }}
        placeholder="농업 데이터를 질문해보세요"
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{
          marginTop: 10,
          padding: "10px 20px",
          fontSize: 16,
          cursor: "pointer",
        }}
      >
        {loading ? "질문 중..." : "질문하기"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* 결과 카드 영역 */}
      {result && (
        <div style={{ marginTop: 30 }}>

          {/* 🤖 AI 답변 카드 */}
          <div style={cardStyle}>
            <h3>🤖 AI 최종 답변</h3>
            <p style={{ whiteSpace: "pre-line" }}>{result.answer}</p>
          </div>

          {/* 🗄 SQL 결과 카드 */}
          {result.sql_result && result.sql_result.length > 0 && (
            <div style={cardStyle}>
              <h3>🗄 SQL 조회 결과</h3>
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr>
                    {Object.keys(result.sql_result[0]).map((key) => (
                      <th
                        key={key}
                        style={tableHeaderStyle}
                      >
                        {key}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.sql_result.map((row, i) => (
                    <tr key={i}>
                      {Object.values(row).map((val, j) => (
                        <td key={j} style={tableCellStyle}>
                          {val}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* 📄 RAG 문서 카드 */}
          {result.rag_docs && result.rag_docs.length > 0 && (
            <div style={cardStyle}>
              <h3>📄 참고 문서 (RAG)</h3>
              <ul>
                {result.rag_docs.map((doc, i) => (
                  <li key={i} style={{ marginBottom: 8 }}>
                    {doc}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

/* ===== 스타일 ===== */

const cardStyle = {
  background: "#f9f9f9",
  padding: 20,
  borderRadius: 8,
  marginBottom: 20,
  boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
};

const tableHeaderStyle = {
  borderBottom: "2px solid #ccc",
  textAlign: "left",
  padding: 8,
};

const tableCellStyle = {
  borderBottom: "1px solid #eee",
  padding: 8,
};

export default App;
