<template>
  <body id="paper">
    <el-form
      class="login-container"
      label-position="left"
      label-width="0px"
      v-loading="loading"
    >
      <h3 class="login_title">用户注册</h3>
      <el-form-item>
        <el-input
          type="text"
          v-model="regInfo.username"
          auto-complete="off"
          placeholder="用户名"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-input
          type="text"
          v-model="regInfo.email"
          auto-complete="off"
          placeholder="邮箱"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-input
          type="password"
          v-model="regInfo.password"
          auto-complete="off"
          placeholder="密码"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-select
          style="width: 100%"
          v-model="valueMember"
          placeholder="选择用户类别"
        >
          <el-option
            v-for="item in optionMember"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item style="width: 100%">
        <router-link to="login">
          <el-button
            type="primary"
            style="
              width: 40%;
              background: #505458;
              border: none;
              margin-right: 10px;
            "
            >返回登录</el-button
          >
        </router-link>
        <el-button
          type="primary"
          style="
            width: 40%;
            background: #505458;
            border: none;
            margin-left: 10px;
          "
          v-on:click="registerSubmit"
          >注册</el-button
        >
      </el-form-item>
    </el-form>
  </body>
</template>


<script>
import { getUsers, postUser } from "../api/api.js";
export default {
  name: "Register",
  data() {
    return {
      loading: false,
      msg: "请选择注册类别",
      optionMember: [
        {
          value: "1",
          label: "我是普通用户",
        },
        {
          value: "2",
          label: "我是店家",
        },
      ],
      valueMember: [],
      regInfo: {
        id: "",
        username: "",
        email: "",
        password: "",
        date: "",
        type: 1,
      },
    };
  },
  methods: {
    loadUsers() {
      getUsers().then((response) => {
        this.userInfos = response.data;
      });
    }, // load books list when visit the page
    registerSubmit() {
      if (this.regInfo.email === "") {
        this.$alert("请输入邮箱", "提示", {
          confirmButtonText: "确定",
        });
        return;
      } else if (this.regInfo.password === "") {
        this.$alert("请输入密码", "提示", {
          confirmButtonText: "确定",
        });
        return;
      } else if (!this.valueMember[0]) {
          this.$alert("请选择用户类别", "提示", {
          confirmButtonText: "确定",
        });
        return;
      }
      var _this = this;
      this.$axios.post('/user/', 
      {
        email: this.regInfo.email, 
        password: this.regInfo.password, 
        username: this.regInfo.username, 
        type: this.valueMember,
        date: this.getMyTime()
      }).then((resp) => {
          if (resp.data.code === 200) {
            this.$alert("注册成功", "提示", {
              confirmButtonText: "确定",
            });
            _this.$router.replace('/login')
          } else {
            this.$alert(resp.data.msg, "提示", {
              confirmButtonText: "确定",
            });
          }
        });
    },
  },
  created: function () {
    this.loadUsers();
  },
};
</script>

<style scoped>
#paper {
  /* background:url("../assets/login.jpg") no-repeat; */
  background-position: center;
  height: 100%;
  width: 100%;
  background-size: cover;
  position: fixed;
}
body {
  margin: -5px 0px;
}
.login-container {
  border-radius: 15px;
  background-clip: padding-box;
  margin: 90px auto;
  width: 350px;
  padding: 35px 35px 15px 35px;
  background: #fff;
  border: 1px solid #eaeaea;
  box-shadow: 0 0 25px #cac6c6;
}
.login_title {
  margin: 0px auto 40px auto;
  text-align: center;
  color: #2c76c0;
}
</style>