<template>
    <div class="register_container">
        <div class="register_box">
            <!--            form-->
            <!--            引用ref-->
            <el-form label-position="left" ref="registerFormRef" :model="registerForm" :rules="registerFormRules" label-width="100px" class="register_form">
                <!--                username-->
                <el-form-item label="邮箱" prop="username">
                    <el-input v-model="registerForm.username"></el-input>
                </el-form-item>
                <!--                nickname-->
                <el-form-item label="昵称" prop="nickname">
                    <el-input v-model="registerForm.nickname"></el-input>
                </el-form-item>
                <!--                password-->
                <el-form-item label="密码" prop="password">
                    <el-input v-model="registerForm.password" type="password"></el-input>
                </el-form-item>
<!--                check password-->
                <el-form-item label="确认密码" prop="checkPass">
                    <el-input v-model="registerForm.checkPass" type="password" autocomplete="off"></el-input>
                </el-form-item>
<!--                ecode-->
                <el-form-item label="验证码" prop="e_code">
                    <el-input v-model="registerForm.e_code"></el-input>
                </el-form-item>
                <!--                button-->
                <el-form-item class="btns">
                    <el-button type="primary" @click="register">注册</el-button>
                    <el-button type="info" @click="resetRegisterForm">重置</el-button>
                    <el-button type="success" @click="sendEcode">发送验证码</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="toLog">
            <el-button @click="toLogin">去登录</el-button>
        </div>
    </div>
</template>

<script>
    export default {
        data(){
            var validateCheckPass = (rule, value, callback) => {
                if (value === ''){
                    callback(new Error('请再次输入密码'));
                } else if (value !== this.registerForm.password){
                    callback(new Error('两次输入密码不一致'));
                } else {
                    callback();
                }
            }
            var validatePass = (rule, value, callback) => {
                if (value.length < 6){
                    callback(new Error('密码不能少于6位'));
                } else {
                    callback();
                }
            }
            var validateUsername = (rule, value, callback) => {
                const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/
                if (regEmail.test(value)) {
                    return callback();
                } else {
                    callback(new Error('请输入合法的邮箱地址'));
                }

            }
            return {
                // 登录表单的数据绑定对象
                registerForm: {
                    username: '',
                    nickname: '',
                    password: '',
                    e_code: ''
                },
                //表单验证规则对象
                registerFormRules: {
                    // 验证用户名
                    username: [
                        { required: true, message: '请输入用户名（有效邮箱地址）', trigger: 'blur' },
                        { validator: validateUsername }
                    ],
                    nickname: [
                        { required: true, message: '请输入昵称', trigger: 'blur' }
                    ],
                    // 验证密码
                    password: [
                        { required: true, message: '请输入密码（至少6位）', trigger: 'blur' },
                        { validator: validatePass }
                    ],
                    e_code: [
                        { required: true, message: '请输入邮箱验证码', trigger: 'blur' }
                    ],
                    checkPass: [
                        {  required: true, trigger: 'blur'},
                        { validator: validateCheckPass }
                    ]
                }
            }
        },
        methods: {
            // 重置表单
            resetRegisterForm() {
                this.$refs.registerFormRef.resetFields();
            },
            // 注册 username, nickname, password, ecode
            register(){
                var vm =this;
                this.$refs.registerFormRef.validate(async valid => {
                    if (valid) {
                        let param = new URLSearchParams();
                        param.append('username', this.registerForm.username);
                        param.append('nickname', this.registerForm.nickname);
                        param.append('password', this.registerForm.password);
                        param.append('ecode', this.registerForm.e_code);
                        this.$http.post('register', param)
                        .then(function (response) {
                            if(response.data === 'ecode-error'){
                                vm.$message.error('验证码错误！');
                            }else if(response.data === 'user-repeated'){
                                vm.$message.error('该邮箱已被注册！');
                            }else if(response.data === 'invalid'){
                                vm.$message.error('用户名或密码无效！');
                            }else if(response.data === 'reg-pass'){
                                vm.$message.success('注册成功！');
                            }else {
                                vm.$message.error('注册失败！');
                            }
                        })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            // 去登录
            toLogin() {
                this.$router.push('/login');
            },
            // 发送邮箱验证码
            sendEcode(){
                var vm = this;
                vm.$message.info("验证码已发出，请稍后")
                this.$http.post('ecode', "username="+this.registerForm.username)
                .then(function(response){
                    console.log(response);
                    if(response.data === 'send-pass') {
                        vm.$message.success('验证码已送达，请验收')
                    } else {
                        vm.$message.error('验证码发送失败')
                    }
                })
                .catch(function(err){
                    console.log(err);
                });

            }
        }
    }
</script>

<style lang="less" scoped>
    .register_container{
        background-image: linear-gradient(to top, #30cfd0 0%, #330867 100%);
        height: 100%;
    }
    .register_box{
        width: 600px;
        height: 450px;
        background-color: #fff;
        border-radius: 6px;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }

    .register_form{
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 10px 100px 10px 50px;
        box-sizing: border-box;
    }

    .btns{
        display: flex;
        justify-content: flex-end;
    }

    .toLog{
        position: absolute;
        top: 10px;
        right: 10px;
    }
</style>
