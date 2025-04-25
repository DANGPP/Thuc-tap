import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { fetchEventDetail, addUserToEvent ,fetchDetailUser } from "../services/detailEventService";
import UserTable from "../components/detailuser_Components/UserTable";
import AddUserPopup from "../components/detailuser_Components/AddUserPopup";
import { Button, Typography, Box, CircularProgress, Alert } from "@mui/material";

function DetailEventPage() {
  const { eventid } = useParams();
  const [eventData, setEventData] = useState(null);
  const [newUser, setNewUser] = useState([]);
  const [showAddUserPopup, setShowAddUserPopup] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [UserPayments,setUserPayments] = useState("")

  useEffect(() => {
    const getEventDetail = async () => {
      try {
        const data = await fetchEventDetail(eventid);
        setEventData(data);
        const userList = await fetchDetailUser(data.id_user_payments);
        setUserPayments(userList);
        
      } catch (err) {
        setError("Lỗi khi tải dữ liệu sự kiện!");
      } finally {
        setLoading(false);
      }
    };

    getEventDetail();
  }, [eventid]);

  const addUser = async (userIds) => {
    try {
      const userToSend = { list_user: userIds || newUser }; // Sử dụng userIds nếu có, nếu không thì dùng newUser
      console.log("Danh sách người gửi:", userToSend);
      await addUserToEvent(eventid, userToSend);
      setShowAddUserPopup(false);
      setNewUser([]); // Reset sau khi thành công
      const updatedData = await fetchEventDetail(eventid);
      setEventData(updatedData);
    } catch (err) {
      setError("Lỗi khi thêm người dùng!");
      throw err; // Ném lỗi để AddUserPopup xử lý nếu cần
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!eventData) return <Typography>Không tìm thấy sự kiện!</Typography>;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Chào mừng đến với sự kiện: {eventData.event_name}
      </Typography>
      <Typography variant="body1">
        <strong>Tổng thu:</strong> {eventData.tong_thu} VND
      </Typography>
      <Typography variant="body1">
        <strong>Số người tham gia:</strong> {eventData.total_users}
      </Typography>
      <Typography variant="body1">
        <strong>Người đã thanh toán Bill:</strong> {UserPayments }
      </Typography>
      <Button
        variant="contained"
        color="primary"
        onClick={() => setShowAddUserPopup(true)}
        sx={{ mt: 2 }}
      >
        + Thêm người
      </Button>
      <UserTable eventData={eventData} setEventData={setEventData} />
      <AddUserPopup
        showAddUserPopup={showAddUserPopup}
        setShowAddUserPopup={setShowAddUserPopup}
        setNewUser={setNewUser}
        addUser={addUser}
        userExist={eventData.users}
      />
    </Box>
  );
}

export default DetailEventPage;