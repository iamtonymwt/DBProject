<template>
  <div>
    <el-dialog
      :show-close="false"
      title="酒店信息"
      :visible.sync="dialogFormVisible"
    >
      <el-form style="text-align: left" ref="dataForm">
        <el-form-item label="酒店名" :label-width="formLabelWidth">
          <el-input
          :placeholder="this.$store.state.user.loc_hotel.name"
            v-model="newHotelName"
          >
          </el-input>
        </el-form-item>
        <el-form-item label="酒店地址" :label-width="formLabelWidth">
          <el-input
            :placeholder="this.$store.state.user.loc_hotel.address"
            v-model="newHotelAddress"
          >
          </el-input>
        </el-form-item>
        <el-form-item label="酒店logo" :label-width="formLabelWidth">
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            action="http://127.0.0.1:8000/upload_logo/"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :on-change="uploadSectionFile"
          >
            <img
              v-if="this.$store.state.user.loc_hotel.piclink"
              :src="this.$store.state.user.loc_hotel.piclink"
              class="avatar"
            />
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </el-form-item>
        <el-form-item label="房间信息" :label-width="formLabelWidth">
          <div>
            <el-checkbox
              v-model="checked_1_room"
              label="单人房"
              border
            ></el-checkbox>
            <div v-show="checked_1_room">
              <span>价格</span>
              <el-input
                size="medium"
                v-model="room_1_price"
                :placeholder="room_1_price_pre"
                label="价格"
              ></el-input>
              <span>总量</span>
              <el-input
                size="medium"
                v-model="room_1_size"
                :placeholder="room_1_size_pre"
                label="总量"
              ></el-input>
            </div>
          </div>

          <div>
            <el-checkbox
              v-model="checked_2_room"
              label="双人房"
              border
            ></el-checkbox>
            <div v-show="checked_2_room">
              <span>价格</span>
              <el-input
                size="medium"
                v-model="room_2_price"
                :placeholder="room_2_price_pre"
                label="价格"
              ></el-input>
              <span>总量</span>
              <el-input
                size="medium"
                v-model="room_2_size"
                :placeholder="room_2_size_pre"
                label="总量"
              ></el-input>
            </div>
          </div>

          <div>
            <el-checkbox
              v-model="checked_3_room"
              label="三人房"
              border
            ></el-checkbox>
            <div v-show="checked_3_room">
              <span>价格</span>
              <el-input
                size="medium"
                v-model="room_3_price"
                :placeholder="room_3_price_pre"
                label="价格"
              ></el-input>
              <span>总量</span>
              <el-input
                size="medium"
                v-model="room_3_size"
                :placeholder="room_3_size_pre"
                label="总量"
              ></el-input>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="注册日期" :label-width="formLabelWidth">
          <el-input
            :placeholder="this.$store.state.user.loc_hotel.regTime"
            :disabled="true"
          >
          </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button v-on:click="myCancel">取消</el-button>
        <el-button v-on:click="myConfirm" type="primary">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "HotelInfoForm",
  components: {},
  data() {
    return {
      dialogFormVisible: false,
      formLabelWidth: "120px",
      newHotelname: "",
      newHotelAddress: "",
      user: {
        id: this.$store.state.user.id,
        email: this.$store.state.user.email,
        username: this.$store.state.user.username,
        hotel: this.$store.state.user.loc_hotel,
        password: "",
        date: this.$store.state.user.date,
      },
      memberList: [],

      checked_1_room: "",
      checked_2_room: "",
      checked_3_room: "",
      room_1_price: "",
      room_1_size: "",
      room_2_price: "",
      room_2_size: "",
      room_3_price: "",
      room_3_size: "",

      room_1_price_pre: "",
      room_1_size_pre: "",
      room_2_price_pre: "",
      room_2_size_pre: "",
      room_3_price_pre: "",
      room_3_size_pre: "",
    };
  },
  created() {
    this.init();
  },
  methods: {
    handleAvatarSuccess(res, file) {
      this.imageUrl = URL.createObjectURL(file.raw);
      console.log(this.imageUrl);
    },
    uploadSectionFile(file) {
      var formData = new FormData();
      formData.append("img", file.raw);
      console.log("try updateLogo");
      this.$axios.post("/upload_logo/", formData).then((resp) => {
        if (resp.date.code === 200) {
          this.$alert("上传成功", "提示", {
            confirmButtonText: "确定",
            // TODO: update img_link
          });
        } else {
          this.$alert("失败", "提示", {
            confirmButtonText: "确定",
          });
        }
      });
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpg";
      const isLt4M = file.size / 1024 / 1024 < 4;

      // if (!isJPG) {
      //   this.$message.error('上传酒店图片只能是 JPG 格式!');
      // }
      if (!isLt4M) {
        this.$message.error("上传酒店图片大小不能超过 4MB!");
      }
      return isLt4M;
    },
    myCancel() {
      this.dialogFormVisible = false;
      this.init();
    },
    async myConfirm() {
      if (this.newHotelname != "") {
        this.user.hotel.name = this.newHotelname;
      }
      if (this.newHotelAddress != "") {
        this.user.hotel.address = this.newHotelAddress;
      }
      if (this.room_1_price !== "") {
        this.user.hotel.roomInfo.single.price = this.room_1_price;
      }
      if (this.room_2_price !== "") {
        this.user.hotel.roomInfo.double.price = this.room_2_price;
      }
      if (this.room_3_price !== "") {
        this.user.hotel.roomInfo.triple.price = this.room_3_price;
      }
      if (this.room_1_size !== "") {
        this.user.hotel.roomInfo.single.size = this.room_1_size;
      }
      if (this.room_2_size !== "") {
        this.user.hotel.roomInfo.double.size = this.room_2_size;
      }
      if (this.room_3_size !== "") {
        this.user.hotel.roomInfo.triple.size = this.room_3_size;
      }
      await this.$axios.post("/updateLocHotel/", this.user).then((resp) => {
        if (resp && resp.data.code === 200) {
          this.$alert("修改酒店信息成功", "提示", {
            confirmButtonText: "确定",
          });
          this.dialogFormVisible = false;
          // this.$store.commit('login',this.user)
        } else {
          this.$alert("修改酒店信息失败", "提示", {
            confirmButtonText: "确定",
          });
        }
      });
      this.$emit("myConfirm");
      this.init();
    },
    init() {
      this.newHotelName = "";
      this.newHotelAddress = "";
      console.log(this.$store.state.user.loc_hotel);
      if (this.$store.state.user.loc_hotel === null) {
        this.checked_1_room = false;
        this.checked_2_room = false;
        this.checked_3_room = false;
        console.log(this.checked_1_room);
        return;
      }
      if (this.$store.state.user.loc_hotel.roomInfo.single != null) {
        this.checked_1_room = true;
        this.room_1_price_pre = this.$store.state.user.loc_hotel.roomInfo.single.price;
        this.room_1_size_pre = this.$store.state.user.loc_hotel.roomInfo.single.amount;
      }
      if (this.$store.state.user.loc_hotel.roomInfo.double != null) {
        this.checked_2_room = true;
        this.room_2_price_pre = this.$store.state.user.loc_hotel.roomInfo.double.price;
        this.room_2_size_pre = this.$store.state.user.loc_hotel.roomInfo.double.amount;
      }
      if (this.$store.state.user.loc_hotel.roomInfo.triple != null) {
        this.checked_3_room = true;
        this.room_3_price_pre = this.$store.state.user.loc_hotel.roomInfo.triple.price;
        this.room_3_size_pre = this.$store.state.user.loc_hotel.roomInfo.triple.amount;
      }
    },
  },
};
</script>

<style scoped>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>