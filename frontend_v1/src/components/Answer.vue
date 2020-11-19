<template>
    <div>
<!--        问题列表-->
        <el-card id="c">
            <div id="c_header">
                <h3>Tons of questions waiting for your answer.</h3>
            </div>
            <div id="queslist">
                <li id="li_id" v-for="(que, index) in ques" class="list-item" style="line-height: 30px">
                    <el-card id="cc">
                        <img id="image" src="../assets/logo.png">
                        <div id="quecontent">
                            <h3><a href="javascript:void(0);" v-on:click="toQuestion(que)">{{que.title}}</a></h3>
                        </div>
                        <div id="answer_bt">
                            <el-button id="answer" type="primary" icon="el-icon-edit" @click="toQuestion(que)">
                                抢首答
                            </el-button>
                        </div>
                        <div class="some_count">
                            <el-button class='some_count_bt' icon="el-icon-view" @click="toQuestion(que)" circle></el-button>&nbsp;{{que.view_count}}
                            <el-button class='some_count_bt' icon="el-icon-star-off" @click="addCollect(que.id)" circle></el-button>&nbsp;{{que.collect_count}}
                        </div>
                    </el-card>
                </li>
            </div>
        </el-card>

<!--        详情对话框-->
        <el-dialog id="dialog" :visible.sync="dialogTableVisible" width="700px">
            <el-card id="question_card">
                <h3>问题详情</h3>
                <!--            问题卡片-->
                <el-card id="que_card">
                    <i class="time">{{cur_que.gmt_create}}+8</i>
                    <el-divider></el-divider>
                    <div id="que_detail">
                        <h3 id="title">{{cur_que.title}}</h3>
                        <div style="margin: 20px 0;"></div>
                        <p id="descript">{{cur_que.description}}</p>
                        <div class="some_count">
                            <el-button class='some_count_bt' icon="el-icon-view" circle></el-button>&nbsp;{{cur_que.view_count}}
                            <el-button class='some_count_bt' icon="el-icon-star-off" @click="addCollect(cur_que.id)" circle></el-button>&nbsp;{{cur_que.collect_count}}
                        </div>
                    </div>
                </el-card>
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


    </div>
</template>

<script>
    export default {
        name: "Answer",
        data() {
            return {
                // 被点击的问题数据
                cur_que: {
                    id: '',
                    title: '',
                    description: '',
                    view_count: '',
                    collect_count: '',
                    gmt_create: ''
                },
                dialogTableVisible: false,
                ques: [
                    // id, title, description, view_count, collect_count, gmt_create
                ],
                // 来自提交表单的数据
                answerArea: ''
            }
        },
        created() {
            this.getData();
        },
        methods: {
            getData() {
                var vm = this;
                this.$http.get('getquestionb')
                    .then(function (response) {
                        var data = response.data.data;
                        data.forEach((item, index) => {
                            vm.ques.push(item);
                        })
                    })
            },
            // 加载问题详情
            toQuestion(que) {
                var username = localStorage.getItem('token');
                this.cur_que.id = que.id;
                this.cur_que.title = que.title;
                this.cur_que.description = que.description;
                this.cur_que.view_count = que.view_count;
                this.cur_que.collect_count = que.collect_count;
                this.cur_que.gmt_create = que.gmt_create;
                var id = que.id;
                // this.$message.success('加载' + id + '号问题！');
                this.dialogTableVisible = true;
                // 浏览记录questoin history
                this.$http.post('addhistory', 'username='+username+'&idq='+id);
            },
            addAnswer(id) {
                // this.$message.success('为' + id + '号问题提交答案');
                var username = localStorage.getItem('token');
                // this.$message.info(username);
                if (this.answerArea === '') {
                    this.$message.error('回答不能为空！');
                } else {
                    // this.$message.success('要提交了！');
                    var vm = this;
                    var content = this.answerArea;
                    this.$http.post('addanswer', 'username=' + username + '&idq=' + id + '&content=' + content)
                        .then(function (response) {
                            if (response.data === 'add-success') {
                                vm.$message.success('提交成功！');
                            } else {
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
            resetInput(){
                this.answerArea = '';
            }
        }
    }
</script>

<style lang="less" scoped>
    .el-main{
        background-image: linear-gradient(to right, #E3FDF5 0%, #FFE6FA 100%);
    }

    .el-button:hover{
        box-shadow: 2px 2px 2px #888888;
    }

    #c{
        margin: 0 auto;
        width: 790px;
        background-image: linear-gradient(to right, #CBBACC 0%, #2580B3 100%);
    }

    #cc{
        margin-left: 20px;
        margin-right: 20px;
    }

    #question_card{
        background-image: linear-gradient(to right, #CBBACC 0%, #2580B3 100%);
    }

    #edit_answer{
        background-image: linear-gradient(-225deg, #CBBACC 0%, #2580B3 100%);
    }

    #image{
        width: 100px;
        float: left;
    }

    #quecontent{
        text-align: left;
        position: relative;
        left: 30px;
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

    a:link {
        text-decoration: none;
        color: black;
    }

    a:hover {
        background-image: linear-gradient(to left, #ffecd2 0%, #fcb69f 100%);
    }

    .dbt{
        padding-right: 20px;
        background-color: #2b4b6b;
        border-width: 0;
        border-radius: 3px;
    }

    .dbt:hover{
        box-shadow: 2px 2px 2px #888888;
    }

    .time{
        font-size: 12px;
        float: right;
    }

    #c_header{
        padding-bottom: 50px;
        height: 50px;
        text-align: left;
    }

    #answer_bt{
        position: relative;
        top: 30px;
    }






</style>