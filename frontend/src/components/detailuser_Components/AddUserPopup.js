import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Autocomplete,
  TextField,
  CircularProgress,
} from "@mui/material";
import { fetchUser } from "../../services/detailEventService";

const AddUserPopup = ({
  showAddUserPopup,
  setShowAddUserPopup,
  setNewUser,
  addUser,
  userExist
}) => {
  const [userList, setUserList] = useState([]); // Danh sách user từ API
  const [selectedUsers, setSelectedUsers] = useState([]); // Danh sách đã chọn
  const [loading, setLoading] = useState(false); // Trạng thái tải dữ liệu

  // Fetch danh sách người dùng khi mở popup
  // useEffect(() => {
  //   if (showAddUserPopup) {
  //     setLoading(true);
  //     fetchUser()
  //       .then((data) => {
  //         setUserList(data);
  //         setLoading(false);
  //       })
  //       .catch(() => setLoading(false));
  //   }
  // }, [showAddUserPopup]);
  useEffect(() => {
    if (showAddUserPopup) {
      setLoading(true);
      fetchUser()
        .then((data) => {
          // Lấy danh sách user_id đã tồn tại
          const existingIds = userExist.map((user) => user.user_id);
  
          // Lọc ra những user chưa tồn tại
          const filteredUsers = data.filter((user) => !existingIds.includes(user.id));
  
          setUserList(filteredUsers);
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }
  }, [showAddUserPopup, userExist]);
  
  // Đóng popup và reset dữ liệu
  const handleClose = () => {
    setShowAddUserPopup(false);
    setSelectedUsers([]);
  };

  // Xử lý khi bấm nút Thêm
  const handleAddUsers = () => {
    const userIds = selectedUsers.map((user) => user.id);
    console.log("Danh sách ID sẽ gửi:", userIds); // Kiểm tra userIds
    setNewUser(userIds); // Cập nhật newUser
    addUser(userIds); // Truyền trực tiếp userIds vào addUser
    handleClose(); // Đóng popup
  };

  return (
    <Dialog open={showAddUserPopup} onClose={handleClose} fullWidth>
      <DialogTitle>Thêm người tham gia</DialogTitle>
      <DialogContent>
        <Autocomplete
          multiple
          options={userList} // Dữ liệu user từ API
          getOptionLabel={(option) => option.name} // Hiển thị tên
          filterSelectedOptions // Không hiển thị những người đã chọn
          value={selectedUsers}
          onChange={(event, newValue) => setSelectedUsers(newValue)}
          loading={loading}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Tìm kiếm và chọn người tham gia"
              margin="dense"
              InputProps={{
                ...params.InputProps,
                endAdornment: (
                  <>
                    {loading ? <CircularProgress size={20} /> : null}
                    {params.InputProps.endAdornment}
                  </>
                ),
              }}
            />
          )}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="error">
          Hủy
        </Button>
        <Button
          onClick={handleAddUsers}
          color="primary"
          disabled={selectedUsers.length === 0 || loading} // Chặn nếu chưa chọn hoặc đang tải
        >
          Thêm
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AddUserPopup;