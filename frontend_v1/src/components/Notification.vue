<template>
    <div>
        <el-card id="c">
            <el-tabs type="border-card">
<!--                未读消息-->
                <el-tab-pane label="未读消息">
                    <div id="notelist_0">
                        <li id="li_id" v-for="(noti, index) in notis_0" class="list-item" style="line-height: 30px">
                            <el-card id="cc">
                                <div id="noti_gmt">{{noti.gmt_create}}</div>
                                <el-divider></el-divider>
                                <div id="noticontent">
                                    <h4>{{noti.content}}</h4>
                                </div>
                                <div id="markbt">
                                    <el-button type="primary" @click="mark(noti)">标为已读</el-button>
                                </div>
                            </el-card>
                        </li>
                    </div>
                </el-tab-pane>
<!--                已读消息-->
                <el-tab-pane label="已读消息">
                    <div id="notelist_1">
                        <li id="li_id" v-for="(noti, index) in notis_1" class="list-item" style="line-height: 30px">
                            <el-card id="cc">
                                <div id="noti_gmt">{{noti.gmt_create}}</div>
                                <el-divider></el-divider>
                                <div id="noticontent">
                                    <h4>{{noti.content}}</h4>
                                </div>
                                <div style="margin: 50px 0;"></div>
                            </el-card>
                        </li>
                    </div>
                </el-tab-pane>
            </el-tabs>
        </el-card>
    </div>
</template>

<script>
    export default {
        name: "Notification",
        data(){
            return {
                // 通知列表（未读）
                notis_0: [
                    // id, content, gmt_create
                ],
                // 通知列表（已读）
                notis_1: [
                    // id, content, gmt_create
                ]
            }
        },
        created() {
            this.getdata();
        },
        methods: {
            getdata(){
                var vm = this;
                var username = localStorage.getItem("token");
                // 获取未读信息列表
                this.$http.get('getnotification0', {params:{username: username}})
                .then(function(response) {
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        vm.notis_0.push(item);
                    })
                });
                // 获取已读信息列表
                this.$http.get('getnotification1', {params:{username: username}})
                .then(function(response) {
                    var data = response.data.data;
                    data.forEach((item, index)=>{
                        vm.notis_1.push(item);
                    })
                });
            },
            mark(noti){
                var vm = this;
                var id = noti.id;
                this.$http.get('markasread', {params:{id: id}})
                .then(function (response) {
                    if(response.data === 'mark-success'){
                        vm.$message.success('标记成功');
                    }else{
                        vm.$message.error('标记失败');
                    }
                })
                this.notis_0 = [];
                this.notis_1 = [];
                this.getdata();
                this.$router.go(0);
            }
        }
    }
</script>

<style lang="less" scoped>
    #c{
        margin: 0 auto;
        width: 790px;
        background-image: linear-gradient(to right, #CBBACC 0%, #2580B3 100%);
    }

    #li_id{
        list-style-type: none;
        margin-bottom: 50px;
    }

    .el-button:hover{
        box-shadow: 2px 2px 2px #888888;
    }
</style>