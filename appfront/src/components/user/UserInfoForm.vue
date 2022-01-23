<template>
    <div>
        <el-dialog
                :show-close="false"
                title="个人信息"
                :visible.sync="dialogFormVisible">
            <el-form  style="text-align: left" ref="dataForm">
                <el-form-item label="用户邮箱" :label-width="formLabelWidth">
                    <el-input
                            :placeholder="this.$store.state.user.email"
                            :disabled="true">
                    </el-input>
                </el-form-item>
                <el-form-item label="用户名" :label-width="formLabelWidth">
                    <el-input
                            :placeholder="this.$store.state.user.username"
                            v-model="newUsername"
                            >
                    </el-input>
                </el-form-item>
                <el-form-item label="是否修改密码" :label-width="formLabelWidth">
                    <el-radio v-model="changePassword" label="1">是</el-radio>
                    <el-radio v-model="changePassword" label="0">否</el-radio>
                    <div v-show="this.changePassword === '1'">
                        <el-input
                                style="margin-top: 10px"
                                placeholder="原密码"
                                v-model="prePassword">
                        </el-input>
                        <el-input
                                style="margin-top: 10px"
                                placeholder="新密码"
                                v-model="newPassword">
                        </el-input>
                    </div>
                </el-form-item>
                <el-form-item label="注册日期" :label-width="formLabelWidth">
                    <el-input
                            :placeholder="this.$store.state.user.date"
                            :disabled="true">
                    </el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button v-on:click="myCancel" >取消</el-button>
                <el-button  v-on:click="myConfirm" type="primary">确定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "UserInfoForm",
        components:{},
        data() {
            return {
                dialogFormVisible:false,
                formLabelWidth:'120px',
                newUsername:'',
                user:{
                    id:this.$store.state.user.id,
                    email:this.$store.state.user.email,
                    username:this.$store.state.user.username,
                    password:'',
                    date:this.$store.state.user.date,
                },
                memberList:[],
                prePassword:'',
                newPassword:'',
                changePassword:'0',
            }
        },
        created() {
            this.init()
        },
        methods:{
            myCancel() {
                this.dialogFormVisible = false
                this.init()
            },
            async myConfirm() {
                var flag = 0
                if (this.changePassword === '1') {
                    if (this.prePassword === '') {
                        this.$alert('请输入原密码', '提示', {
                            confirmButtonText: '确定'
                        })
                        return
                    }
                    if (this.newPassword === '') {
                        this.$alert('新密码不能为空', '提示', {
                            confirmButtonText: '确定'
                        })
                        return
                    }
                    await this.$axios //通过登录接口验证原密码是否正确
                        .post('/Login', {
                            email: this.$store.state.user.email,
                            password: this.prePassword
                        })
                        .then(resp => {
                            if (resp && resp.data.code === 200) {
                                this.user.password = this.newPassword
                            }
                            else {
                                this.$alert('原密码错误', '提示', {
                                    confirmButtonText: '确定'
                                })
                                flag = 1;
                            }
                        })
                }
                if (flag === 1) {
                    return
                }
                if (this.newUsername !== '') {
                    this.user.username = this.newUsername
                }
                await this.$axios
                    .post('/updateUser/',this.user)
                    .then(resp => {
                        if (resp && resp.data.code === 200) {
                            this.$alert('修改个人信息成功', '提示', {
                                confirmButtonText: '确定'
                            })
                            this.dialogFormVisible = false
                            // this.$store.commit('login',this.user)
                        }
                        else {
                            this.$alert('修改个人信息失败', '提示', {
                                confirmButtonText: '确定'
                            })
                        }
                    })
                this.$emit('myConfirm')
                this.init()
            },
            init() {
                this.newUsername = ''
                this.prePassword = ''
                this.newPassword = ''
                this.changePassword = '0'
                this.memberList = []
            }
        }
    }
</script>

<style scoped>
</style>