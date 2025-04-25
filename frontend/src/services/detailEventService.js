const API_BASE_URL_2 = process.env.REACT_APP_API_BACKEND + "events/"
const API_BASE_URL_USER = process.env.REACT_APP_API_BACKEND + "users"
// lấy status của người tham gia sự kiện
export const fetchUserStatus = async (eventid, userid) => {
    try {   
        const response = await fetch(`${API_BASE_URL_2}${eventid}/users/${userid}`);
        if (!response.ok) throw new Error("Lỗi khi lấy dữ liệu status người dùng");
        const data = await response.json();
        return data.status; // Trả về status của người dùng
    } catch (error) {
        console.error("Lỗi khi fetch dữ liệu của láy status:", error);
        return null;
    }
}
//sửa status của người tham gia sự kiện
export const updateUserStatus = async (eventid, userid, status) => {
    try {
        const response = await fetch(`${API_BASE_URL_2}${eventid}/users/${userid}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ status }), // Gửi trạng thái mới
        });

        if (!response.ok) throw new Error("Lỗi khi cập nhật trạng thái người dùng");

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Lỗi khi cập nhật trạng thái:", error);
        return null;
    }
};
export const fetchEventDetail = async (eventid) =>{
    try{
        // const response = await fetch(`${API_BASE_URL_2}${eventid}`);
        const response = await fetch(API_BASE_URL_2+eventid+"/users")
        if (!response.ok) throw new Error("lỗi khi lấy dữ liệu");
        const data = await response.json();
        return data;
    }
    catch (error){
        console.error("Lỗi khi fetch dữ liệu:", error);
      return [];
    }
}
// gửi thông báo
export const fetchsendmail = async(eventid,userid)=>{
    try{
        const response = await fetch(API_BASE_URL_2+"send-email/"+eventid+"/"+userid,{
            method: "POST"
            
        });

        console.log("📩 Phản hồi từ server:", response); // Kiểm tra phản hồi từ server

        if (!response.ok) {
            throw new Error(`Lỗi khi gửi mail ở detailEventService gửi mail: ${response.statusText}`);
          }
      
          const responseData = await response.json(); // Đọc dữ liệu JSON từ phản hồi
          console.log("✅ Dữ liệu JSON từ API:", responseData); // Kiểm tra nội dung JSON trả về
      
          return responseData;
    }
    catch(error){
        console.error("❌ Lỗi khi gọi API  gửi mail ở detailEventService gửi mail:", error);
    return null;
    }
}
// lấy user
export const fetchUser = async () =>{
    try{
       
        const response = await fetch(API_BASE_URL_USER)
        if (!response.ok) throw new Error("lỗi khi lấy dữ liệu");
        const data = await response.json();
        return data;
    }
    catch (error){
        console.error("Lỗi khi fetch dữ liệu user của detailEventService.js:", error);
      return [];
    }
}


// Lấy chi tiết user 
export const fetchDetailUser = async(userid)=>{
    try{
        const response = await fetch(API_BASE_URL_USER+"/"+userid)
        if (!response.ok) throw new Error("lỗi khi lấy dữ liệu chi tiet cua user");
        const data = await response.json();
        return data.name;
    }
    catch (error){
        console.error("lỗi:", error)
    }
}
// thêm người vào sự kiện
export const addUserToEvent = async(eventid,user)=>{
    try{
        const response = await fetch(API_BASE_URL_2+eventid+"/users",{
            method: "POST",
            headers:{
                "Content-Type": "application/json",
            },
            body: JSON.stringify(user)
        });

        console.log("📩 Phản hồi từ server:", response); // Kiểm tra phản hồi từ server

        if (!response.ok) {
            throw new Error(`Lỗi khi thêm người vào sự kiện: ${response.statusText}`);
          }
      
          const responseData = await response.json(); // Đọc dữ liệu JSON từ phản hồi
          console.log("✅ Dữ liệu JSON từ API:", responseData); // Kiểm tra nội dung JSON trả về
      
          return responseData;
    }
    catch(error){
        console.error("❌ Lỗi khi gọi API thêm sự kiện:", error);
    return null;
    }
}
export const delUserfromEvent= async(eventid,listUser)=>{
    try{
        const response = await fetch(API_BASE_URL_2+eventid+"/users",{
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(listUser)
        });
        console.log("📩 Phản hồi từ server:", response); // Kiểm tra phản hồi từ server

        if (!response.ok) {
            throw new Error(`Lỗi khi xóa người khỏi sự kiện: ${response.statusText}`);
          }
      
          const responseData = await response.json(); // Đọc dữ liệu JSON từ phản hồi
          console.log("✅ Dữ liệu JSON từ API:", responseData); // Kiểm tra nội dung JSON trả về
      
          return responseData;
    }
    
    catch(error){
        console.error("❌ Lỗi khi gọi API xóa người dùng:", error);
        return null;
    }
}
export const adjustBonus = async(eventid,userid,bonusthem)=>{
    try{
        const response = await fetch(API_BASE_URL_2+eventid+"/users/"+userid,{
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(bonusthem)
        });
        console.log("📩 Phản hồi từ server:", response); // Kiểm tra phản hồi từ server

        if (!response.ok) {
            throw new Error(`Lỗi khi chỉnh sửa bonus: ${response.statusText}`);
          }
      
          const responseData = await response.json(); // Đọc dữ liệu JSON từ phản hồi
          console.log("✅ Dữ liệu JSON từ API:", responseData); // Kiểm tra nội dung JSON trả về
      
          return responseData;
    }
    
    catch(error){
        console.error("❌ Lỗi khi gọi API chỉnh sửa bonus:", error);
        return null;
    }
}