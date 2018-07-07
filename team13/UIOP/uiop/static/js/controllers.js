/**
 * Created by ShellyXia on 18/3/25.
 */

angular.module('myApp.controllers', ['ngFileUpload', 'ngFileSaver'])
    //home
    .controller('homeCtrl', function($rootScope, $scope, $http) {
        $rootScope.hostUrl = '13.59.213.150';
        // $rootScope.hostUrl = 'localhost:8000';

        console.log(isLogin);
        console.log(notLogin);
        enter_Channel = false;

        if (!notLogin == true) {
            $("#isLogin").css("display",'none');
            $("#notLogin").css("display", 'block');
            $("#setting-wrapper").css("display", 'block');
        } else {
            $("#isLogin").css("display",'block');
            $("#notLogin").css("display", 'none');
            $("#setting-wrapper").css("display", 'none');
            $rootScope.username = "";
            $rootScope.token = "";
        }

        if (isLogin && enter_Channel) {
            $("#settingChannel").css("display", 'block');
        } else {
            $("#settingChannel").css("display", 'none');
        }

        $(document).ready(function() {
            $("#sn1").focus();
            var $inputCollection = $('.digit-input');
                $inputCollection.each(function(index) {
                $(this).keyup(function(e) {
                    var keyCode = e.keyCode;
                    if(isValued(keyCode)){
                        if($(this).val().length < 1) {
                            $inputCollection.eq((index + $inputCollection.length - 1) % $inputCollection.length).focus();
                        } else {
                            $inputCollection.eq((index + 1) % $inputCollection.length).focus();
                        }
                    }
                });
            });
        })

        $scope.enterChannel = function() {
            if ($("#sn1").val() == "" || $("#sn2").val() == "" || $("#sn3").val() == "" || $("#sn4").val() == "") {
                $.alert("Please enter the full code for the channel!");
            } else {
                var codeChannel = $("#sn1").val() + $("#sn2").val() + $("#sn3").val() + $("#sn4").val();
                $http.get("http://" + $rootScope.hostUrl + "/uiop/channel/"+codeChannel , {
                    params: {
                        username: $rootScope.username
                    },
                    cache: false
                })
                    .success(function(ret) {
                        if (ret.message != null) {
                            $.alert(ret.message);
                        } else {
                            $.cookie('channel_code', codeChannel);
                            console.log(ret.success + " qwe" + ret.needPassword);
                            if (ret.success == "false" && ret.needPassword == "true") {
                                $.alert("Need Password");
                                $rootScope.channel_temp_code = codeChannel;
                                window.location.href = "#enterPassword/" + codeChannel;
                            } else {
                                $rootScope.channel = ret;
                                $rootScope.channel.channel_code = codeChannel;
                                $rootScope.channel.newfileList = ret.newfileList;
                                $rootScope.channel.expiration_time = ret.expirationTime;
                                $rootScope.channel.lectureMode = ret.lecturerMode;
                                window.location.href = "#channel/"+codeChannel;
                            }
                        }
                    })
                    .error(function() {
                        $.alert('Failed to access because of network error.')
                    });
            }
        }

        $scope.createChannel = function () {
            $scope.password = $("#password_channel").val();

            if($("#lectureMode").prop("checked")) {
                $scope.lectureMode = true;
            } else {
                $scope.lectureMode = false;
            }
            // alert($scope.lectureMode);

            if ($rootScope.user == null) {
                $http.post("http://" + $rootScope.hostUrl + "/uiop/create-channel",
                    JSON.stringify({
                        // username: $rootScope.username,
                        // token: $rootScope.token,
                        password: $scope.password,
                        mode: $scope.lectureMode,
                        owner: $rootScope.username
                    }))
                    .success(function(ret) {
                        $rootScope.channel = ret;
                        $rootScope.channel.newfileList = [];
                        $rootScope.channel.password = $scope.password;
                        $rootScope.channel.lectureMode = $scope.lectureMode;
                        $rootScope.channel.owner = $rootScope.username;
                        $rootScope.channel.expiration_time = ret.expirationTime;
                        enter_Channel = true;
                        window.location.href = "#channel/" + $rootScope.channel.channel_code;
                    })
                    .error(function() {
                        $.alert('Failed to access because of network error.')
                    });
            }
        }

        $scope.logout = function () {
            isLogin = false;
            notLogin = true;
            enter_Channel = false;
            $rootScope.username = "";
            window.location.href = "#home";
            $.cookie('username', null);
        }

    })

    //Channel
    .controller('channelCtrl', function($rootScope, $scope, Upload, $interval, $http, FileSaver, Blob, $stateParams){

        //update parameters
        enter_Channel = true;
        $scope.codeChannel = $stateParams.channel_code;

        if (typeof($rootScope.username) != "undefined")
            $scope.username = $rootScope.username;
        else {
            //alert("here")
            if (typeof($.cookie('username'))=="undefined"){
                // alert("here")
                $scope.username = ""
                $rootScope.username = "";
            }
            else {
                $scope.username = $.cookie('username');
                $rootScope.username = $.cookie('username');
            }
            if($scope.username.length > 0) {
                isLogin = true;
                notLogin = false;
            } else {
                isLogin = false;
                notLogin = true;
            }
            console.log(isLogin + " " + notLogin);
            $rootScope.hostUrl = '13.59.213.150';
            //$rootScope.hostUrl = 'localhost:8000'

            $.ajax({
            url: "http://" + $rootScope.hostUrl + "/uiop/channel/" + $scope.codeChannel,
            type: 'GET',
            data: {
                "username":  $scope.username
            },
            async:false,
            dataType: "json",
            success: function(ret){
                if (ret.message != null) {
                    $.alert(ret.message);
                    } else {
                    console.log(ret.success + " qwe" + ret.needPassword);
                    if (ret.success == "false" && ret.needPassword == "true") {
                        $.alert("Need Password");
                        $rootScope.channel_temp_code = $scope.codeChannel;
                        window.location.href = "#enterPassword/" + $scope.codeChannel;
                        } else {
                        $rootScope.channel = ret;
                        $rootScope.channel.channel_code = $scope.codeChannel;
                        $rootScope.channel.newfileList = ret.newfileList;
                        $scope.expire_time = $rootScope.channel.expirationTime;
                        window.location.href = "#channel/" + $scope.codeChannel;
                    }}
            },
            error: function (result) {
                $.alert('Failed to access because of network error.')
            }
        });

        }

        //console.log($stateParams.channel_code + "&&&" + $scope.username);

        console.log($rootScope.channel);
        console.log("isLogin + enterChannel:" + isLogin + enter_Channel);
        console.log($rootScope.username)
        if (isLogin && enter_Channel) {
            $("#isLogin").css("display",'none');
            $("#notLogin").css("display", 'block');
            if ($rootScope.channel.owner === $rootScope.username) {
                $("#loginOwner").css("display", 'inline-block');
                $("#settingChannel").css("display", 'block');
            } else {
                $("#loginOwner").css("display", 'none');
                $("#settingChannel").css("display", 'none');
            }
        } else {
            $("#isLogin").css("display",'block');
            $("#notLogin").css("display", 'none');
            $("#setting-wrapper").css("display", 'none');
        }

        var timestamp = new Date().getTime();
        $scope.channelURL = window.location.href;

        $rootScope.channel && console.log($rootScope.channel.newfileList);

        $scope.itemList = $rootScope.channel ? $rootScope.channel.newfileList : [];
        $scope.expire_time = $rootScope.channel.expirationTime;


        if ($rootScope.channel.lectureMode == false) {
            $("#gridRadios1").prop('checked','checked');
        } else {
             $("#gridRadios2").prop('checked','checked');
        }

        //send request to add a person
        $http.post("http://" + $rootScope.hostUrl + "/uiop/add-person/" + $rootScope.channel.channel_code,
            JSON.stringify({}))
            .success(function (ret) {
                $scope.channel_online_number = ret.channel_online_number;
            })
            .error(function() {
                $.alert('Failed to access because of network error.')
            });
        //$scope.itemList = [{fileName: "test.pdf", fileAddress: "test", fileType: "pdf"}, {fileName: "test.pdf", fileAddress: "test", fileType: "pdf"}];

        //updateChannel every five seconds
        var oneTimer = $interval(function() {
            //send post request to update new files
            console.log(333);
            $http.post('http://' + $rootScope.hostUrl + '/uiop/pull-new-file/' + $rootScope.channel.channel_code,
                JSON.stringify({
                    timestamp: timestamp
                })
            ).success(function(ret) {
                // alert(timestamp);
                console.log(111);
                if (ret.newfileList.length > 0) {
                    //$scope.newfileList = ret.newfileList;
                    $scope.itemList = ret.newfileList;
                }
            }).error(function() {
                $.alert('Failed to access because of network error.')
            });

            //send get request to check the expire status of the channel & online people
            $http.get("http://" + $rootScope.hostUrl + "/uiop/update-channel-info/" + $rootScope.channel.channel_code , {
                params: {},
                cache: false
            })
                .success(function(ret) {
                    //alert("success!");
                    $scope.channel_online_number = ret.channel_online_number;
                    if (ret.lecturerMode == "True") {
                        //alert("finally")
                        $scope.lectureMode = true;
                        $rootScope.channel.lectureMode = true;
                    }
                    else {
                        $scope.lectureMode = false;
                        $rootScope.channel.lectureMode = false;
                    }

                    if (ret.active == "False") {
                        $.alert("This channel is expired.");
                        window.location.href = "#home";
                    }
                    $scope.expire_time = ret.expirationTime;
                })
                .error(function() {
                    $.alert('Failed to access because of network error.')
                });
            timestamp = new Date().getTime();
            //$scope.itemList = [{fileName: "test2.pdf", fileAddress: "test2", fileType: "excel"}, {fileName: "test2.pdf", fileAddress: "test", fileType: "excel"}, {fileName: "test.pdf", fileAddress: "test", fileType: "pdf"}];
        }, 5 * 1000);

        //uploadFile
        $scope.uploadFiles = function(files, errFiles) {
            console.log("test");
            console.log($rootScope.channel.lectureMode);
            //alert($rootScope.username +" "+ $rootScope.channel.owner + " "+ $rootScope.channel.lecturerMode);
            if (($rootScope.username != $rootScope.channel.owner) && (($rootScope.channel.lectureMode == "True")||($rootScope.channel.lectureMode == true))) {
                $.alert("This is the lecture mode. You cannot upload the file.");
            } else {
                $scope.files = files;
                $scope.errFiles = errFiles;
                angular.forEach(files, function(file) {
                    file.upload = Upload.upload({
                        url: 'http://'+ $rootScope.hostUrl +'/uiop/upload/' + $rootScope.channel.channel_code,
                        data: {
                            file: file
                        }
                    }).success(function(ret) {
                        $.alert(ret.message);
                        //Send request to update the new files
                        $http.post('http://' + $rootScope.hostUrl + '/uiop/pull-new-file/' + $rootScope.channel.channel_code,
                            JSON.stringify({
                                timestamp: timestamp
                            })
                        ).success(function(ret) {
                            //alert(timestamp);
                            if (ret.newfileList.length > 0) {
                                $scope.itemList = ret.newfileList;
                            }
                        }).error(function() {
                            $.alert('Failed to access because of network error.')
                        });
                        timestamp = new Date().getTime();
                    }).error(function() {
                        $.alert('Failed to access because of network error.')
                    });
                });
            }
        }

        //popup window for settings
        $scope.updateChannel = function() {
            var selectedMode = $('input:radio:checked').val();
            $scope.lectureMode = selectedMode;
            $scope.channel_password = $("#channel_password").val();
            $scope.duration_time = $("#duration_time").val();

            console.log($scope.lectureMode + " " + $scope.channel_password + " " + $scope.duration_time);

            $http.post("http://" + $rootScope.hostUrl + "/uiop/modify-channel/" + $rootScope.channel.channel_code,
                JSON.stringify({
                    username: $rootScope.username,
                    password: $scope.channel_password,
                    mode: $scope.lectureMode,
                    expire_time: $scope.duration_time
                }))
                .success(function(ret) {
                    if (ret.success == false) {
                        $.alert(ret.message);
                    }
                    else {
                        $rootScope.channel.lectureMode = ret.lecturermode;
                        $rootScope.channel.channel_password = ret.password;
                        $rootScope.channel.expirationTime = ret.expire_time;
                    }
                })
                .error(function() {
                    $.alert('Failed to access because of network error.')
                });
        }

        //expire the channel right now
        $scope.expireNow = function() {
            $.alert("expire Successful!");
            //send get request for expire now
            $http.get("http://" + $rootScope.hostUrl + "/uiop/expire-now/" + $rootScope.channel.channel_code , {
                params: {},
                cache: false
            })
                .success(function(ret) {
                    $.alert(ret.message);
                    window.location.href = "#home";
                })
                .error(function() {
                    $.alert('Failed to access because of network error.');
                });
        }

        //when the channel page is closed, the interval request will be destroyed and the online_number will minus one.
        $scope.$on('$destroy',function(){
            $interval.cancel(oneTimer);
        });

        $scope.logout = function () {
            isLogin = false;
            notLogin = true;
            enter_Channel = false;
            $rootScope.username = "";
            window.location.href = "#home";
            $.cookie('username', null);
        }

    })

    //enterChannelPassword
    .controller('enterChannelPasswordCtrl', function($scope, $http, $rootScope) {
        enter_Channel = false;
        if (isLogin && enter_Channel) {
            $("#isLogin").css("display",'none');
            $("#notLogin").css("display", 'block');
            if ($rootScope.channel.owner === $rootScope.username) {
                $("#loginOwner").css("display", 'inline-block');
                $("#settingChannel").css("display", 'block');
            } else {
                $("#loginOwner").css("display", 'none');
            }
        } else {
            $("#isLogin").css("display",'block');
            $("#notLogin").css("display", 'none');
            $("#setting-wrapper").css("display", 'none');
        }


        $scope.matchChannelPassword = function() {

            $http.post('http://' + $rootScope.hostUrl + '/uiop/channel/' + $rootScope.channel_temp_code,
                JSON.stringify({
                    password: $scope.password
                })
            ).success(function (ret) {
                if (ret.errorMessage != null) {
                    $.alert(ret.errorMessage);
                } else {
                    //$.alert('success??');
                    $rootScope.channel = ret;
                    $rootScope.channel.channel_code = $rootScope.channel_temp_code;
                    window.location.href = "#channel/" + $rootScope.channel.channel_code;
                }
            }).error(function() {
                $.alert('Failed to access because of network error.')
            });
        };

        $scope.logout = function () {
            isLogin = false;
            notLogin = true;
            enter_Channel = false;
            $rootScope.username = "";
            window.location.href = "#home";
            $.cookie('username', null);
        }

    })

    //Login
    .controller('loginCtrl', function($scope, $http, $rootScope) {
        //alert("asdsadsa");
        var error = document.getElementById("login-error");

        isLogin = false;
        notLogin = true;
        enter_Channel = false;
        $rootScope.username = "";
        if (!notLogin == true) {
            $("#isLogin").css("display",'none');
            $("#notLogin").css("display", 'block');
        } else {
            $("#isLogin").css("display",'block');
            $("#notLogin").css("display", 'none');
            $rootScope.username = "";
            $rootScope.token = "";
        }

        if (isLogin && enter_Channel) {
            $("#settingChannel").css("display", 'block');
        } else {
            $("#settingChannel").css("display", 'none');
        }

        $scope.userLogin = function() {
            error.innerHTML = "";
            $http.post('http://' + $rootScope.hostUrl + '/uiop/login',
                JSON.stringify({
                    username: $scope.username,
                    password: $scope.password
                })
            ).success(function (ret) {
                //console.log(ret[0].success + " "+ ret[0].message);
                $scope.success = ret.success;
                if (ret.success == true) {
                    $rootScope.username = $scope.username;
                    $rootScope.token = ret.token;
                    isLogin = true;
                    notLogin = false;
                    $.cookie('username', $scope.username);
                    window.location.href = "#home";
                } else {
                    error.innerHTML = "username and password don't match!";
                }
            }).error(function() {
                $.alert('Failed to access because of network error.')
            });
        };

    })

    //Signup
    .controller('signupCtrl', function($scope, $http, $rootScope) {
        //alert("asdsadsa");
        var error = document.getElementById("login-error");
        enter_Channel = false;

        if (isLogin && enter_Channel) {
            $("#settingChannel").css("display", 'block');
        } else {
            $("#settingChannel").css("display", 'none');
        }

        $scope.userRegister = function() {

            console.log($scope.username, $scope.password);

            error.innerHTML = "";
            $http.post('http://' + $rootScope.hostUrl + '/uiop/register',
                JSON.stringify({
                    username: $scope.username,
                    password: $scope.password
                })
            ).success(function (ret) {
                //console.log("here");
                //alert("success@!!!!!")
                $scope.success = ret.success;
                console.log($scope.success);
                //console.log(ret);
                if (ret.success == true) {
                    $rootScope.username = $scope.username;
                    $.cookie('username', $scope.username);
                    isLogin = true;
                    notLogin = false;
                    window.location.href = "#home";
                } else {
                    error.innerHTML = "username already exists!";
                }
            }).error(function() {
                $.alert('Failed to access because of network error.')
                });
            }
    })

    //Profile
    .controller('profileCtrl', function($scope, $rootScope, $http) {


        $scope.username = $.cookie('username');


        $http.post('http://' + $rootScope.hostUrl + '/uiop/get-user-channel-list',
            JSON.stringify({
                username: $scope.username,
            })
        ).success(function (ret) {
            console.log(ret.channelList);
            $scope.channelList = ret.channelList;
        }).error(function() {
            $.alert('Failed to access because of network error.')
        });

        $scope.modifyUserPassword = function () {
            $http.post('http://' + $rootScope.hostUrl + '/uiop/modify-user-password',
                JSON.stringify({
                    username: $scope.username,
                    old: $scope.oldpassword,
                    new: $scope.newpassword
                })
            ).success(function (ret) {
                $.alert(ret.message);
               this.newpassword = null;
               this.oldpassword = null;
            }).error(function() {
                $.alert('Failed to access because of network error.')
            });
        }

        $scope.logout = function () {
            isLogin = false;
            notLogin = true;
            enter_Channel = false;
            $rootScope.username = "";
            window.location.href = "#home";
            $.cookie('username', null);
        }
    })


function isValued(keyCode) {
    if ((keyCode >= 48 && keyCode <= 57) || (keyCode >= 65 && keyCode <= 90) || (keyCode >= 96 && keyCode <= 105)) {
        return true;
    } else
        return false;
}
