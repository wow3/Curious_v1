<template>
    <div class="login_container">
        <div class="login_box">
<!--            photo-->
            <div class="avatar_box">
                <img src="../assets/logo.png" alt="">
            </div>
<!--            form-->
<!--            引用ref-->
            <el-form ref="loginFormRef" :model="loginForm" :rules="loginFormRules" label-width="0px" class="login_form">
<!--                username-->
                <el-form-item prop="username">
                    <el-input v-model="loginForm.username" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
<!--                password-->
                <el-form-item prop="password">
                    <el-input v-model="loginForm.password" prefix-icon="el-icon-lock" type="password"></el-input>
                </el-form-item>
<!--                button-->
                <el-form-item class="btns">
                    <el-button type="primary" @click="login">登录</el-button>
                    <el-button type="info" @click="resetLoginForm">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="toReg">
            <el-button @click="toRegister">注册</el-button>
        </div>
    </div>
</template>

<script>
    export default {
        data(){
            return {
                // 登录表单的数据绑定对象
                loginForm: {
                    username: '',
                    password: ''
                },
                //表单验证规则对象
                loginFormRules: {
                    // 验证用户名
                    username: [
                        { required: true, message: '请输入用户名', trigger: 'blur' }
                    ],
                    // 验证密码
                    password: [
                        { required: true, message: '请输入密码', trigger: 'blur' }
                    ]
                }
            }
        },
        methods: {
            // 表单重置
            resetLoginForm() {
                // console.log(this)
                this.$refs.loginFormRef.resetFields();
            },
            // 登录成功
            slogin(){
                // 登录成功之后将token保存到客户端的sessionStorage中
                // 项目中除了登录之外的其他API接口，必须在登录之后才能访问
                // token只在当前网站打开期间生效，所以token保存在sessionStorage中
                localStorage.setItem("token", this.loginForm.username);
                // 编程式导航跳转到主页
                this.$router.push('/home');
            },
            alogin(){
                this.$router.push('/admin');
            },
            // 登录
            login() {
                this.$refs.loginFormRef.validate(async valid => {
                    if(!valid) return;
                    var vm = this;
                    this.$http.post('login', 'username='+this.loginForm.username+'&password='+this.loginForm.password)
                    .then(function (response) {
                        console.log(response)
                        if(response.data === 'login-fail'){
                            vm.$message.error('登录失败！');
                            return;
                        }else if(response.data === 'admin'){
                            vm.alogin();
                            return;
                        }else if(response.data === 'user-not-exist'){
                            vm.$message.error('用户名不存在！');
                            return;
                        }else if(response.data === 'banned'){
                            vm.$notify({
                                title: 'info',
                                message: '该账户涉嫌违规操作，已被管理员封禁。',
                                type: 'warning',
                                duration: 0
                            });
                        }else{
                                localStorage.setItem("nickname", response.data)
                                vm.$message.success('登录成功！');
                                vm.slogin();
                        }
                    })
                })
            },
            // 注册
            toRegister() {
                this.$router.push('/register');
            }
        }
    }
</script>

<style lang="less" scoped>
    .login_container{
        background-image: linear-gradient(to top, #30cfd0 0%, #330867 100%);
        height: 100%;
    }
    .login_box{
        width: 450px;
        height: 300px;
        background-color: #fff;
        border-radius: 6px;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);

        .avatar_box{
            height: 130px;
            width: 130px;
            border: 1px solid #eee;
            border-radius: 50%;
            padding: 10px;
            box-shadow: 0 0 10px #ddd;
            position: absolute;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #fff;
            img{
                width: 100%;
                height: 100%;
                border-radius: 50%;
                background-color: #eee;
            }
        }
    }

    .login_form{
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 0 20px;
        box-sizing: border-box;
    }

    .btns{
        display: flex;
        justify-content: flex-end;
    }

    .toReg{
        position: absolute;
        top: 10px;
        right: 10px;
    }
</style>
