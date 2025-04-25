import React, { useState } from "react";
import EditBonusPopup from "./editbonusPopup";
import { delUserfromEvent, fetchEventDetail, fetchsendmail,fetchUserStatus,updateUserStatus } from "../../services/detailEventService";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Typography,
  Box,
  Snackbar, 
  Alert,
  Switch
} from "@mui/material";

const UserTable = ({ eventData, setEventData }) => {
  const [showPopup, setShowPopup] = useState({ status: false, userid: "" });
  const [bonusType, setBonusType] = useState("none");
  const [bonusValue, setBonusValue] = useState("");
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState("success"); // "success", "error", "info", "warning"

  const handleSendNotice = async (event_id, user_id) => {
    try {
      setSnackbarMessage("Đang gửi...");
      setSnackbarSeverity("info");
      setSnackbarOpen(true);
  
      // Gọi fetchsendmail thay vì gọi API trực tiếp
      const task_id = await fetchsendmail(event_id, user_id);
  
      // Poll kết quả task
      const pollStatus = async () => {
        const res = await fetch(`/task-status/${task_id}`);
        const statusData = await res.json();
  
        if (statusData.state === "SUCCESS") {
          setSnackbarMessage("Gửi thành công!");
          setSnackbarSeverity("success");
          setSnackbarOpen(true);
        } else if (statusData.state === "FAILURE") {
          setSnackbarMessage("Gửi thất bại!");
          setSnackbarSeverity("error");
          setSnackbarOpen(true);
        } else {
          // Nếu chưa xong, đợi rồi kiểm tra lại
          setTimeout(pollStatus, 1000);
        }
      };
  
      pollStatus();
    } catch (error) {
      setSnackbarMessage("Có lỗi xảy ra!");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
    }
  };


  if (!eventData || !eventData.users) {
    return <Typography>Không có dữ liệu sự kiện.</Typography>;
  }

  const openPopup = (iduser) => setShowPopup({ status: true, userid: iduser });
  const closePopup = () => {
    setShowPopup({ status: false, userid: null });
    setBonusType("none");
    setBonusValue("");
  };
  // Xóa tất cả người dùng
  const handleDeleteAll = async () => {
    for (const user of eventData.users) {
      if (user.status !== "Người đã thanh toán") {
        await delUserfromEvent(eventData.event_id, { list_del_us: [user.user_id] });
      }
    }
    const updatedData = await fetchEventDetail(eventData.event_id);
    setEventData(updatedData);
  };
  // Gửi thông báo cho tất cả người dùng
  const handleSendAllNotices = async () => {
    for (const user of eventData.users) {
      await handleSendNotice(eventData.event_id, user.user_id);
    }
  };
  return (
    <>
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Box display="flex" justifyContent="space-between" p={2}>
        <Button variant="contained" color="error" onClick={handleDeleteAll}>
          Delete All
        </Button>
        <Button variant="contained" color="primary" onClick={()=>{
          handleSendAllNotices()
        }}>
          Send All Notices
        </Button>
      </Box>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Stt</TableCell>
            <TableCell>User ID</TableCell>
            <TableCell>Tên</TableCell>
            <TableCell>Bonus</TableCell>
            <TableCell>Số tiền phải trả</TableCell>
            <TableCell>Hành động</TableCell>
            <TableCell>Trạng thái</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {eventData.total_users > 0 &&
            eventData.users.map((user, index) => (
              <TableRow key={user.user_id}>
                <TableCell>{index + 1}</TableCell>
                <TableCell>{user.user_id}</TableCell>
                <TableCell>{user.name}</TableCell>
                <TableCell>
                  <Button variant="contained" color="secondary" onClick={() => openPopup(user.user_id)}>
                    Bonus Options
                  </Button>
                </TableCell>
                <TableCell>{user.bill_due} VND</TableCell>
                <TableCell>
                  {user.status!=="Người đã thanh toán" &&
                    <Button
                    variant="contained"
                    color="error"
                    onClick={async () => {
                      await delUserfromEvent(eventData.event_id, { list_del_us: [user.user_id] });
                      const updatedData = await fetchEventDetail(eventData.event_id);
                      setEventData(updatedData);
                    }}
                  >
                    Delete
                  </Button>
                  }
                  <Button variant="contained" color="primary" sx={{ ml: 1 }}
                   onClick={() => handleSendNotice(eventData.event_id, user.user_id)}
                  >
                    Send Notice
                  </Button>
                </TableCell>
                {/* <TableCell sx={{ color: user.status === "UnPaid" ? "red" : "green" }}>
                  {user.status}
                </TableCell> */}
                
{/* <TableCell>
  <Switch
    checked={user.status === "Người đã thanh toán"}
    onChange={() => {
      const updatedStatus =
        user.status === "Người đã thanh toán" ? "UnPaid" : "Người đã thanh toán";

      // Cập nhật trạng thái trong danh sách user
      const updatedUsers = eventData.users.map((u) =>
        u.user_id === user.user_id ? { ...u, status: updatedStatus } : u
      );

      // Gọi hàm setEventData để cập nhật lại UI
      setEventData({ ...eventData, users: updatedUsers });
    }}
    color="success"
  />
  <Typography
    variant="body2"
    sx={{
      color: user.status === "UnPaid" ? "red" : "green",
      ml: 1,
      display: "inline",
    }}
  >
    {user.status === "Người đã thanh toán" ? "Paid" : "UnPaid"}
  </Typography>
</TableCell> */}
<TableCell>
  {user.status === "Người đã thanh toán" ? (
    <Typography
      variant="body2"
      sx={{
        color: "green",
        ml: 1,
        display: "inline",
      }}
    >
      Người đã thanh toán
    </Typography>
  ) : (
    <>
      <Switch
        checked={user.status === "Paid"}
        onChange={async () => {
          let updatedStatus;
          if (user.status === "Paid") {
            updatedStatus = "UnPaid";
          } else if (user.status === "UnPaid") {
            updatedStatus = "Paid";
          }

          const result = await updateUserStatus(eventData.event_id, user.user_id, updatedStatus);

          if (result) {
            const updatedUsers = eventData.users.map((u) =>
              u.user_id === user.user_id ? { ...u, status: updatedStatus } : u
            );
            setEventData({ ...eventData, users: updatedUsers });
          } else {
            alert("Không thể cập nhật trạng thái.");
          }
        }}
        color="success"
      />
      <Typography
        variant="body2"
        sx={{
          color: user.status === "UnPaid" ? "red" : "green",
          ml: 1,
          display: "inline",
        }}
      >
        {user.status}
      </Typography>
    </>
  )}
</TableCell>
              </TableRow>
            ))}
        </TableBody>
      </Table>

      {/* Import Popup */}
      <EditBonusPopup
        showPopup={showPopup}
        closePopup={closePopup}
        bonusType={bonusType}
        setBonusType={setBonusType}
        bonusValue={bonusValue}
        setBonusValue={setBonusValue}
        eventid={eventData.event_id}
        userid={showPopup.userid}
        setEventData={setEventData}
      />
    </TableContainer>
    <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}>
      <Alert
        onClose={() => setSnackbarOpen(false)}
        severity={snackbarSeverity}
        sx={{ width: "100%" }}>
        {snackbarMessage}
      </Alert>
    </Snackbar>

    </>
  );
};

export default UserTable;
