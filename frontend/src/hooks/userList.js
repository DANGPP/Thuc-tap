import { useState, useEffect } from "react";
import { fetchUser } from "../services/detailEventService"; 
export const useFetchUsers = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getUsers = async () => {
      try {
        const data = await fetchUser();
        setUsers(data);
        setError(null);
      } catch {
        setError("Lỗi khi lấy danh sách người dùng!");
      } finally {
        setLoading(false);
      }
    };

    getUsers();
  }, []); // Chạy 1 lần khi component mount

  return { users, loading, error };
};
