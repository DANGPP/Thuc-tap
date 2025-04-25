
import React from "react";
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button, Autocomplete } from "@mui/material";
import { useFetchUsers } from "../../hooks/userList";
const AddEventPopup = ({ showAddPopup, setShowAddPopup, newEvent, handleInputChange, addEvent, setNewEvent }) => {
  const { users, loading } = useFetchUsers();
  if (!showAddPopup) return null;
  
  return (
    <Dialog open={showAddPopup} onClose={() => setShowAddPopup(false)}>
      <DialogTitle>Thêm sự kiện</DialogTitle>
      <DialogContent>
        <TextField
          fullWidth
          margin="dense"
          label="Tên sự kiện"
          name="name"
          value={newEvent.name}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          margin="dense"
          type="date"
          name="date"
          value={newEvent.date}
          onChange={handleInputChange}
          InputLabelProps={{ shrink: true }}
        />
        <TextField
          fullWidth
          margin="dense"
          label="Giá bill"
          name="total_bill"
          value={newEvent.total_bill}
          onChange={handleInputChange}
        />
        {/* <TextField
          fullWidth
          margin="dense"
          label="Người thanh toán"
          name="id_user_payments"
          value={newEvent.id_user_payments}
          onChange={handleInputChange}
        /> */}
        <Autocomplete
          options={users}
          getOptionLabel={(option) => option.name} // Hiển thị tên người dùng
          loading={loading}
          onChange={(event, newValue) => {
            handleInputChange({
              target: { name: "id_user_payments", value: newValue ? newValue.id : "" },
            });
          }}
          renderInput={(params) => (
            <TextField
              {...params}
              fullWidth
              margin="dense"
              label="Người thanh toán"
            />
          )}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={() => {
          setShowAddPopup(false);
          setNewEvent({ name: "", date: "", total_bill: "", id_user_payments: "" });
        }} color="secondary">
          Hủy
        </Button>
        <Button onClick={addEvent} color="primary" variant="contained">
          Thêm
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AddEventPopup;