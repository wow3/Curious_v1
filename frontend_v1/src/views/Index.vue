<template>
    <el-container class="home_container">
<!--        头部-->
        <el-header>
            <div class="title">
                <img id="logo" src="../assets/logo.png" alt="">
            </div>
            <div class="nav">
                <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect" router>
                    <el-menu-item index="/home">Home</el-menu-item>
                    <el-menu-item index="/answer">Answer</el-menu-item>
                    <el-menu-item index="/space">Space</el-menu-item>
                    <el-menu-item index="/notification">Notification</el-menu-item>
                    <el-menu-item index="/profile">Profile</el-menu-item>
                </el-menu>
            </div>

            <div>
                <el-input id="scin" v-model="searchkey" placeholder="输入问题关键字" prefix-icon="el-icon-search" ></el-input>
            </div>
            <div id="scbt">
                <el-button id="searchbt" slot="append" icon="el-icon-search" @click="doSearch"></el-button>
            </div>
            <div id="addqbt">
                <el-button id="add" type="primary" icon="el-icon-edit" @click="dialogFormVisible = true">Add Question</el-button>
            </div>
            <div>
                <div id="wel_text">Welcome！</div><img id="avatar" :src="userinfo.avatar_url" alt="form.nickname">
            </div>
            <el-button id="out" type="info" @click="logout">退出</el-button>
        </el-header>
        <el-main>
<!--            路由占位符-->
            <router-view></router-view>
        </el-main>
<!--        新增问题对话框-->
        <el-dialog title="提问" :visible.sync="dialogFormVisible">
            <el-form ref="formRef" :model="form" label-position="left" :rules="formRules">
                <el-form-item label="标题" :label-width="formLabelWidth">
                    <el-input v-model="form.title" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="问题分类" :label-width="formLabelWidth">
                    <el-select v-model="form.category" placeholder="请选择问题分类">
                        <el-option label="校园" value="campus"></el-option>
                        <el-option label="焦点" value="focus"></el-option>
                        <el-option label="财经" value="finance"></el-option>
                        <el-option label="科技" value="technology"></el-option>
                        <el-option label="文化" value="culture"></el-option>
                        <el-option label="教育" value="education"></el-option>
                        <el-option label="深度" value="depth"></el-option>
                        <el-option label="娱乐" value="entertain"></el-option>
                        <el-option label="时尚" value="fashion"></el-option>
                        <el-option label="体育" value="sports"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="问题描述" :label-width="formLabelWidth">
                    <el-input type="textarea" :rows="10" v-model="form.description" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button class="dbt" type="primary" @click="addQuestion">提 交</el-button>
                <el-button class="dbt" type="primary" @click="resetForm">重 置</el-button>
            </div>
        </el-dialog>
<!--        搜索结果对话框-->
        <el-dialog id="search_dialog" :visible.sync="searchDialogVisible">
            <div div="search_list">
                <li id="li_id" v-for="(que, index) in ques">
                    <el-card id="que_card">
                        <img id="image" src="../assets/logo.png">
                        <div id="que_content">
                            <h3><a href="javascript:void(0);" v-on:click="toQuestion(que)">{{que.title}}</a></h3>
                        </div>
                        <div style="margin: 60px 0;"></div>
                        <div class="some_count">
                            <el-button class='some_count_bt' icon="el-icon-view" @click="toQuestion(que)" circle></el-button>&nbsp;{{que.view_count}}
                            <el-button class='some_count_bt' icon="el-icon-star-off" @click="addCollect(que.id)" circle></el-button>&nbsp;{{que.collect_count}}
                            <el-button class='some_count_bt' icon="el-icon-chat-line-round" @click="toQuestion(que)" circle></el-button>&nbsp;{{que.answer_count}}
                        </div>
                    </el-card>
                </li>
            </div>
        </el-dialog>

<!--        详情对话框-->
        <el-dialog id="dialog" :visible.sync="dialogTableVisible" width="700px">
            <el-card id="question_card">
                <h3>问题详情</h3>
                <!--            问题卡片-->
                <el-card id="que_card">
                    <i class="time">{{cur_que.gmt_create}}</i>
                    <el-divider></el-divider>
                    <div id="que_detail">
                        <h3 id="title">{{cur_que.title}}</h3>
                        <div style="margin: 20px 0;"></div>
                        <p id="descript">{{cur_que.description}}</p>
                        <div style="margin: 20px 0;"></div>
                        <div class="some_count">
                            <el-button class='some_count_bt' icon="el-icon-view" circle></el-button>&nbsp;{{cur_que.view_count}}
                            <el-button class='some_count_bt' icon="el-icon-star-off" @click="addCollect(cur_que.id)" circle></el-button>&nbsp;{{cur_que.collect_count}}
                        </div>
                    </div>
                </el-card>
            </el-card>
            <div style="margin: 50px 0;"></div>
            <!--            回答列表-->
            <el-card id="answer_card">
                <div id="answer_list" >
                    <h3>回答列表</h3>
                    <li id="in_li_id" v-for="(ans, index) in cur_que.answers" style="line-height: 30px">
                        <el-card id="in_card">
                            <div class="card_head">
                                <img class="avatar" src="../assets/logo.png">
                                <i class="author">{{ans.username}}</i>
                                <i class="time">{{ans.gmt_create}}+8</i>
                            </div>
                            <el-divider></el-divider>
                            <div id="in_content">
                                <p>{{ans.content}}</p>
                            </div>
                            <div class="some_count">
                                <el-button class='some_count_bt' icon="el-icon-s-opportunity" @click="addUpvote(ans.id)" circle></el-button>&nbsp;{{ans.upvote}}
                            </div>
                        </el-card>
                    </li>
                </div>
            </el-card>
            <div style="margin: 50px 0;"></div>
            <!--            编辑回答卡片-->
            <el-card id="edit_answer">
                <!--                回答键入区域-->
                <el-input type="textarea" :autosize="{ minRows: 5, maxRows: 100}" placeholder="请输入内容" v-model="answerArea"></el-input>
                <div style="margin: 20px 0;"></div>
                <div id="dbts">
                    <el-button class="dbt" type="primary" @click="addAnswer(cur_que.id)">提 交</el-button>
                    <el-button class="dbt" type="primary" @click="resetInput">重 置</el-button>
                </div>
            </el-card>
        </el-dialog>

    </el-container>

</template>

<script>

export default {
    name: 'Index',
    data(){
        return {
            activeIndex: '/home',
            dialogFormVisible: false,
            searchDialogVisible: false,
            dialogTableVisible: false,
            searchkey: '',
            form: {
                username: '',
                nickname: '',
                title: '',
                category: '',
                description: ''
            },
            formLabelWidth: '100px',
            formRules: {
                // 验证标题
                title: [
                    { required: true, message: '请输入标题', trigger: 'blur' }
                ],
                // 验证描述
                description: [
                    { required: true, message: '请输入问题描述', trigger: 'blur' }
                ]
            },
            // search result
            ques: [],
            cur_que: {
                id: '',
                title: '',
                description: '',
                view_count: '',
                collect_count: '',
                gmt_create: '',
                answers: [
                    // id, username, content, upvote, time
                ]
            },
            answerArea: '',
            userinfo: {
                username: '',
                avatar_url: '',
                age: ''
            }
        }
    },
    created() {
       this.getUserInfo();
    },
    mounted() {
        this.form.username = localStorage.getItem("token");
        this.form.nickname = localStorage.getItem("nickname");
    },
    methods: {
        // 切换menu
        handleSelect(key, keyPath){
            console.log(key, keyPath)
        },
        // 注销
        logout(){
            localStorage.clear()
            this.$router.push('/login')
        },
        // 提问
        addQuestion() {
            if(this.form.username !== '' && this.form.category!== '' && this.form.description !== ''){
                var vm = this;
                this.$http.post('addquestion', 'username='+this.form.username+'&title='+this.form.title+'&category='+this.form.category+'&description='+this.form.description)
                .then(function (response) {
                    if(response.data === 'add-success'){
                        vm.$message.success('提交成功！');
                    }else{
                        vm.$message.error('提交失败!');
                    }
                })
            }else{
                this.$message.error('请将问题信息补充完整');
            }
        },
        // 搜索动作触发，发送请求，填充ques
        doSearch(){
            var vm = this;
            this.ques = [];
            if(this.searchkey === ''){
                vm.$message.error('请输入问题关键字');
            }else{
                this.$http.get('search', {params: {key: vm.searchkey}})
                .then(function (response) {
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        vm.ques.push(item);
                    })
                })
                this.searchDialogVisible = true;
            }
        },
        toQuestion(que){
            var username = localStorage.getItem('token');
            this.cur_que.id = que.id;
            this.cur_que.title = que.title;
            this.cur_que.description = que.description;
            this.cur_que.view_count = que.view_count;
            this.cur_que.collect_count = que.collect_count;
            this.cur_que.gmt_create = que.gmt_create;
            var id = que.id;
            // this.$message.success('加载'+id+'号问题！');
            var vm = this;
            this.cur_que.answers = [];
            // 加载id问题的回答
            this.$http.get('getanswer', {params:{idq: id}})
                .then(function (response) {
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        console.log(item);
                        vm.cur_que.answers.push(item);
                    })
                })
            this.dialogTableVisible = true;
            // 浏览记录questoin history
            this.$http.post('addhistory', 'username='+username+'&idq='+id);
        },
        // 提交回答  username, idq, content
        addAnswer(id){
            // this.$message.success('为'+id+'号问题提交答案');
            var username = localStorage.getItem('token');
            // this.$message.info(username);
            if(this.answerArea === ''){
                this.$message.error('回答不能为空！');
            }else{
                // this.$message.success('要提交了！');
                var vm = this;
                var content = this.answerArea;
                this.$http.post('addanswer', 'username='+username+'&idq='+id+'&content='+content)
                    .then(function (response) {
                        if(response.data === 'add-success'){
                            vm.$message.success('提交成功！');
                        }else{
                            vm.$message.error('提交失败!');
                        }
                    })
            }
            // 回答通知notification
            this.$http.get('newanswer', {params: {idq: id}});
        },
        addCollect(id){
            var username = localStorage.getItem('token');
            var idq = id;
            var vm = this;
            this.$http.post('addcollection', 'username='+username+'&idq='+idq)
                .then(function (response) {
                    if(response.data === 'success'){
                        vm.$message.success('收藏+1');
                    }else{
                        vm.$message.error('请勿重复收藏。');
                    }
                })
        },
        addUpvote(id){
            var username = localStorage.getItem('token');
            var ida = id;
            var vm = this;
            // 提交点赞
            this.$http.post('addupvote', 'username='+username+'&ida='+ida)
                .then(function (response) {
                    if(response.data === 'success'){
                        vm.$message.success('点赞+1');
                    }else{
                        vm.$message.error('请勿重复点赞。');
                    }
                })
            // 点赞通知notification
            this.$http.get('newupvote', {params: {username: username, ida: ida}})
        },
        resetInput(){
            this.answerArea = '';
        },
        // 表单重置
        resetForm() {
            this.form.title='';
            this.form.description='';
            this.form.category='';
        },
        getUserInfo(){
            this.userinfo.username = localStorage.getItem('token');
            var vm = this;
            this.$http.get('getuserinfo', {params: {username: vm.userinfo.username}})
                .then(function (response) {
                    var data = response.data.data;
                    vm.userinfo.age = data.age;
                    vm.userinfo.avatar_url = require('../assets/avatar/'+data.avatar_url);
                })
        }
    }
}
</script>

<style lang="less" scoped>
    .el-header{
        background-color: #fff;
        display: flex;
        justify-content: space-between;
        padding-left: 0.7cm;
        align-items: center;
        color: #2b4b6b;
        font-size: 16px;
        font-weight: bold;
    }

    .title{
        display: flex;
        align-items: center;
        span {
            margin-left: 15px;
        }
    }

    .nav{
        position: relative;
        left: -30px;
    }

    #out{
        background-color: #606060;
    }


    .el-button:hover{
        box-shadow: 2px 2px 2px #888888;
    }

    .el-main{
        background-image: linear-gradient(-225deg, #7085B6 0%, #87A7D9 50%, #DEF3F8 100%);
    }

    .home_container{
        height: 100%;
    }

    #logo{
        height: 60px;
        border-radius: 10px;
    }

    #add{
        background-color: #3b5b7b;
    }

    .dbt{
        background-color: #3b5b7b;
    }


    #search{
        width: 200px;
    }

    #avatar{
        width: 45px;
        height: 45px;
        border-radius: 50%;
    }

    #wel_text{
        float: left;
        position: relative;
        top: 15px;
    }

    #scbt{
        position: relative;
        right: 70px;
    }

    #searchbt{
        background-color: #2b4b6b;
    }


    a:link {
        text-decoration: none;
        color: black;
    }

    a:hover {
        background-image: linear-gradient(to left, #ffecd2 0%, #fcb69f 100%);
    }

    #image{
        width: 100px;
        float: left;
    }

    .some_count{
        float: right;
        padding-bottom: 10px;
    }

    .some_count_bt{
        border: 1px solid #7bbfea;
    }


    #li_id{
        list-style-type: none;
        margin-bottom: 50px;
    }

    #que_content{
        text-align: left;
        position: relative;
        left: 30px;
    }

    #question_card{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
    }

    #answer_card{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
    }

    #edit_answer{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
    }

    #in_li_id{
        list-style-type: none;
        margin-bottom: 30px;
    }

    .avatar{
        height: 10px;
        border-radius: 5px;
    }

    .time{
        font-size: 12px;
        float: right;
    }

</style>