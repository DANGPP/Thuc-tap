
import React from "react";
import { adjustBonus, fetchEventDetail } from "../../services/detailEventService";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Radio,
  RadioGroup,
  FormControlLabel,
  TextField,
} from "@mui/material";

const EditBonusPopup = ({
  showPopup,
  closePopup,
  bonusType,
  setBonusType,
  bonusValue = "", // Giá trị mặc định
  setBonusValue,
  eventid,
  userid,
  setEventData,
}) => {
  if (!showPopup.status) return null;

  const handleOkClick = async () => {
    try {
      let result = {};
      if (bonusType === "percent" && bonusValue) {
        result = { bonusthem: `${bonusValue}%` };
      } else if (bonusType === "extra" && bonusValue) {
        result = { bonusthem: bonusValue };
      } else if (bonusType === "none") {
        result = { bonusthem: "0" };
      }
      await adjustBonus(eventid, userid, result);
      closePopup();
      const updatedData = await fetchEventDetail(eventid);
      setEventData(updatedData);
    } catch (error) {
      console.error("Error adjusting bonus:", error);
    }
  };

  const handleBonusValueChange = (e) => {
    const value = e.target.value;
    // Chỉ cho phép số hoặc chuỗi rỗng
    if (value === "" || !isNaN(value)) {
      setBonusValue(value);
    }
  };

  return (
    <Dialog open={showPopup.status} onClose={closePopup} fullWidth>
      <DialogTitle>Bonus Options</DialogTitle>
      <DialogContent>
        <RadioGroup value={bonusType} onChange={(e) => setBonusType(e.target.value)}>
          <FormControlLabel value="none" control={<Radio />} label="None" />
          <FormControlLabel value="percent" control={<Radio />} label="Ủng hộ theo % bill:" />
          {bonusType === "percent" && (
            <TextField
              type="number"
              // value={bonusValue}
              onChange={handleBonusValueChange}
              inputProps={{ min: 0 }}
              sx={{ mt: 1 }}
              fullWidth
            />
          )}
          <FormControlLabel value="extra" control={<Radio />} label="Ủng hộ thêm:" />
          {bonusType === "extra" && (
            <TextField
              type="number"
              // value={bonusValue}
              onChange={handleBonusValueChange}
              inputProps={{ min: 0 }}
              sx={{ mt: 1 }}
              fullWidth
            />
          )}
        </RadioGroup>
      </DialogContent>
      <DialogActions>
        <Button onClick={closePopup} color="error">Hủy</Button>
        <Button onClick={handleOkClick} color="primary">OK</Button>
      </DialogActions>
    </Dialog>
  );
};

export default EditBonusPopup;