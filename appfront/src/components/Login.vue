<template>
    <body id="poster">
        <el-form class="login-container" label-position="left" label-width="0px">
            <h3 class="login_title">系统登录</h3>
            <el-form-item>
                <el-input type = "text" v-model="loginForm.mail"
                        auto-complete="off" placeholder="邮箱"></el-input>
            </el-form-item>
            <el-form-item>
                <el-input type="password" v-model="loginForm.password"
                        auto-complete="off" placeholder="密码"></el-input>
            </el-form-item>
            <el-form-item style="width: 100%">
                <el-button type="primary" style="width:40%;background: #505458;
                        border:none;margin-right: 10px" @click="Login" >登录</el-button>
                <el-button type="primary" style="width:40%;background: #505458;
                        border:none;margin-right: 10px" @click="Register" >注册</el-button>
            </el-form-item>
        </el-form>
    </body>
</template>

<script>
    import {login} from '../api/api.js';
    export default {
        name: 'login',
        data () {
            return {
                loginForm: {
                    mail: '983499284@qq.com',
                    password: '123'
                },
                responseResult: [],
                msg : "",
            }
        },
        methods: {
            Login () {
                var _this = this;
                let data = this.loginForm
                login(data).then((resp) => {
                    this.msg = resp.data.msg
                    if (resp.data.code == 200) { //登录成功
                        console.log(resp.data.userInfo);
                        this.$store.commit('login', resp.data.userInfo);
                        console.log(this.$store.state.user)
                        this.$router.replace("/Home");
                    } else {
                        this.loginForm.password = "";
                        this.loginForm.mail = "";
                        this.$alert('用户名或密码错误', '提示', {
                            confirmButtonText: '确定'
                        })
                    }
                }).catch((err) => {
                    console.log(err);
                });
            },

            Register() {
                this.$router.replace("/Register")
            }
        }
    }
</script>
<style>
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
        color: #505458;
    }
    #poster {
        /* background:url("../assets/login.jpg") no-repeat; */
        background-position: center;
        height: 100%;
        width: 100%;
        background-size: cover;
        position: fixed;
    }
    body{
        margin: 0px;
    }
</style>