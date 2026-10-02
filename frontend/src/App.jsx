import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

function App() {
  const [books, setBooks] = useState([]);
  const [members, setMembers] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [status, setStatus] = useState("");

  const loadData = async () => {
    try {
      const [booksRes, membersRes, transactionsRes] = await Promise.all([
        axios.get(`${API}/books`),
        axios.get(`${API}/members`),
        axios.get(`${API}/transactions`)
      ]);

      setBooks(booksRes.data);
      setMembers(membersRes.data);
      setTransactions(transactionsRes.data);
      setStatus("Backend connected successfully");
    } catch (error) {
      setStatus("Backend connection failed");
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>Online Library Management System</h1>

      <p><strong>Status:</strong> {status}</p>

      <hr />

      <h2>Books ({books.length})</h2>
      <ul>
        {books.map((book) => (
          <li key={book.id}>
            {book.title} — {book.author} — Available: {book.available_quantity}
          </li>
        ))}
      </ul>

      <h2>Members ({members.length})</h2>
      <ul>
        {members.map((member) => (
          <li key={member.id}>
            {member.name} — {member.email}
          </li>
        ))}
      </ul>

      <h2>Transactions ({transactions.length})</h2>
      <ul>
        {transactions.map((transaction) => (
          <li key={transaction.id}>
            Book ID: {transaction.book_id} | Member ID: {transaction.member_id} | Status: {transaction.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;