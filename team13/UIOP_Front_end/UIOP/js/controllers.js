/**
 * Created by ShellyXia on 18/3/25.
 */

angular.module('myApp.controllers', ['ngFileUpload', 'ngFileSaver'])
    //home
    .controller('homeCtrl', function($rootScope, $scope, $http) {
        $rootScope.hostUrl = 'localhost';

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

        $('input.digit-input').keyup(function(){
            var c=$(this);
            if(/[^\d]/.test(c.val())){//replace non number
                var temp_amount=c.val().replace(/[^\d]/g,'');
                $(this).val(temp_amount);
            }
        })

        $(document).ready(function() {
            $("#sn1").focus();
            $("input[name^='sn']").each(function() {
                $(this).keyup(function() {
                    if ($(this).val().length > 0) {
                        $(this).next().focus();
                    }
                })
            })
        })

        $scope.enterChannel = function() {
            if ($("#sn1").val() == "" || $("#sn2").val() == "" || $("#sn3").val() == "" || $("#sn4").val() == "") {
                $.alert("Please enter the full code for the channel!");
            } else {
                var codeChannel = $("#sn1").val() + $("#sn2").val() + $("#sn3").val() + $("#sn4").val();
                $http.get("http://" + $rootScope.hostUrl + ":8000/uiop/channel/"+codeChannel , {
                    params: {
                        username: $rootScope.username
                    },
                    cache: false
                })
                    .success(function(ret) {
                        if (ret.message != null) {
                            $.alert(ret.message);
                        } else {
                            console.log(ret.success + " qwe" + ret.needPassword);
                            if (ret.success == "false" && ret.needPassword == "true") {
                                $.alert("Need Password");
                                $rootScope.channel_temp_code = codeChannel;
                                window.location.href = "#enterPassword/" + codeChannel;
                            } else {
                                $rootScope.channel = ret;
                                $rootScope.channel.channel_code = codeChannel;
                                $rootScope.channel.newfileList = ret.newfileList;
                                window.location.href = "#channel/"+codeChannel;
                            }
                        }
                    })
                    .error(function() {
                        $.alert('Failed to access because of network error.')
                    });
            }
        }

        if($("#lectureMode").prop("checked")) {
            $scope.lectureMode = true;
        } else {
            $scope.lectureMode = false;
        }

        $scope.password = $("#password_channel").val();

        $scope.createChannel = function () {
            if ($rootScope.user == null) {
                $http.post("http://" + $rootScope.hostUrl + ":8000/uiop/create-channel",
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
                        enter_Channel = true;
                        window.location.href = "#channel/"+$rootScope.channel.channel_code;
                    })
                    .error(function() {
                        $.alert('Failed to access because of network error.')
                    });
            }
        }

    })

    //Channel
    .controller('channelCtrl', function($rootScope, $scope, Upload, $interval, $http, FileSaver, Blob){

        //update parameters
        enter_Channel = true;

        var timestamp = new Date().getTime();
        $scope.channelURL = window.location.href;

        $scope.channel_online_number = 100;//$rootScope.channel.channel_online_number

        console.log($rootScope.channel.owner + " " +  $rootScope.username);
        if (isLogin && enter_Channel) {
            console.log("isLogin + enterChannel:" + isLogin + enter_Channel);
            $("#settingChannel").css("display", 'block');
            console.log()
            if ($rootScope.channel.owner == $rootScope.username) {
                $("#loginOwner").css("display", 'inline-block');
            } else {
                $("#loginOwner").css("display", 'none');
            }
        }

        //send request to add a person
        $http.post("http://" + $rootScope.hostUrl + ":8000/uiop/add-person/" + $rootScope.channel.channel_code,
            JSON.stringify({}))
            .success(function (ret) {
                $scope.channel_online_number = ret.channel_online_number;
            })
            .error(function() {
                $.alert('Failed to access because of network error.')
            });

        $rootScope.channel && console.log($rootScope.channel.newfileList);

        $scope.itemList = $rootScope.channel ? $rootScope.channel.newfileList : [];
        //$scope.itemList = [{fileName: "test.pdf", fileAddress: "test", fileType: "pdf"}, {fileName: "test.pdf", fileAddress: "test", fileType: "pdf"}];

        //downloadFile send request
        $scope.downloadFile = function (fileAddress, fileType, fileName) {
            console.log($rootScope.channel.channel_code)
            $http.post("http://" + $rootScope.hostUrl + ":8000/uiop/download/" + $rootScope.channel.channel_code,
                JSON.stringify({
                    fileAddress: fileAddress
                }, {responseType: 'arraybuffer'}))
                .success(function (ret, status, headers) {
                    if (ret.success == false) {
                        $.alert(ret.message);
                    }
                    else {
                        var header = headers(

                        );
                        var fileType = header['content-type'];
                        var blob = new Blob([ret], { type: "image/png"});
                        //change download.pdf to the name of whatever you want your file to be
                        saveAs(blob, fileName);
                    }
                })
                .error(function() {
                    $.alert('Failed to access because of network error.')
                });
        }

        //updateChannel every five seconds
        var oneTimer = $interval(function() {
            //send post request to update new files
            console.log(333);
            $http.post('http://' + $rootScope.hostUrl + ':8000/uiop/pull-new-file/' + $rootScope.channel.channel_code,
                JSON.stringify({
                    timestamp: timestamp
                })
            ).success(function(ret) {
                // alert(timestamp);
                console.log(111);
                if (ret.newfileList.length > 0) {
                    //$scope.newfileList = ret.newfileList;
                    $scope.itemList = ret.newfileList;
                    // angular.forEach($scope.newfileList, function (file) {
                    //     $scope.itemList.push(file);
                    // })
                }
            }).error(function() {
                $.alert('Failed to access because of network error.')
            });

            //send get request to check the expire status of the channel & online people
            $http.get("http://" + $rootScope.hostUrl + ":8000/uiop/update-channel-info/" + $rootScope.channel.channel_code , {
                params: {},
                cache: false
            })
                .success(function(ret) {
                    //alert("success!");
                    $scope.channel_online_number = ret.channel_online_number;
                    if (ret.active == false) {
                        $.alert("This channel is expired.");
                        window.location.href = "#home";
                    }
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
            console.log($rootScope.channel);
            //alert($rootScope.username +" "+ $rootScope.channel.owner + " "+ $rootScope.channel.lecturerMode);
            if (($rootScope.username != $rootScope.channel.owner) && ($rootScope.channel.lecturerMode == "True")) {
                $.alert("You cannot upload the file.");
            } else {
                $scope.files = files;
                $scope.errFiles = errFiles;
                angular.forEach(files, function(file) {
                    file.upload = Upload.upload({
                        url: 'http://localhost:8000/uiop/upload/' + $rootScope.channel.channel_code,
                        data: {
                            file: file
                        }
                    }).success(function(ret) {
                        $.alert(ret.message);
                        //Send request to update the new files
                        $http.post('http://' + $rootScope.hostUrl + ':8000/uiop/pull-new-file/' + $rootScope.channel.channel_code,
                            JSON.stringify({
                                timestamp: timestamp
                            })
                        ).success(function(ret) {
                            //alert(timestamp);
                            if (ret.newfileList.length > 0) {
                                $scope.itemList = ret.newfileList;
                                //$scope.newfileList = ret.newfileList;
                                // angular.forEach($scope.newfileList, function (file) {
                                //     $scope.itemList.push(file);
                                // })
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

            $http.post("http://" + $rootScope.hostUrl + ":8000/uiop/modify-channel/" + $rootScope.channel.channel_code,
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
                        $rootScope.channel.lectureMode = ret.mode;
                        $rootScope.channel.channel_password = ret.password;
                        $rootScope.channel.expirationTime = ret.expire_time;
                    }
                })
                .error(function() {
                    $.alert('Failed to access because of network error.')
                });
        }

        //popup window for QRcode
        $scope.getQRCode = function() {

        }

        //expire the channel right now
        $scope.expireNow = function() {
            $.alert("expire Successful!");
            //send get request for expire now
            $http.get("http://" + $rootScope.hostUrl + ":8000/uiop/expire-now/" + $rootScope.channel.channel_code , {
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

            //send request to minus a person
            $http.post("http://" + $rootScope.hostUrl + ":8000/uiop/minus-person/" + $rootScope.channel.channel_code,
                JSON.stringify({}))
                .success(function (ret) {
                    $scope.channel_online_number = 100;//ret.channel_online_number;
                })
                .error(function() {
                    $.alert('Failed to access because of network error.')
                });
        });

    })

    //enterChannelPassword
    .controller('enterChannelPasswordCtrl', function($scope, $http, $rootScope) {
        //alert("asdsadsa");

        enter_Channel = false;
        if (isLogin && enter_Channel) {
            $("#settingChannel").css("display", 'block');
        } else {
            $("#settingChannel").css("display", 'none');
        }

        $scope.matchChannelPassword = function() {

            $http.post('http://' + $rootScope.hostUrl + ':8000/uiop/channel/' + $rootScope.channel_temp_code,
                JSON.stringify({
                    password: $scope.password
                })
            ).success(function (ret) {
                //console.log(ret[0].success + " "+ ret[0].message);
                if (ret.errorMessage != null) {
                    $.alert(ret.errorMessage);
                } else {
                    $.alert('success');
                    $rootScope.channel = ret;
                    $rootScope.channel.channel_code = $rootScope.channel_temp_code;
                    window.location.href = "#channel/" + $rootScope.channel.channel_code;
                }
            }).error(function() {
                $.alert('Failed to access because of network error.')
            });
        };

        $scope.logout = function () {
            //alert("11111");
            isLogin = false;
            notLogin = true;
            enter_Channel = false;
            $rootScope.username = "";
            window.location.href = "#home";
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
            $http.post('http://' + $rootScope.hostUrl + ':8000/uiop/login',
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
                    window.location.href = "#home";
                } else {
                    error.innerHTML = "username and passward don't match!";
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
            $http.post('http://' + $rootScope.hostUrl + ':8000/uiop/register',
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
                    $rootScope.token = ret.token;
                    isLogin = true;
                    notLogin = false;
                    window.location.href = "#home";
                } else {
                    error.innerHTML = "username is already exsited!";
                }
            }).error(function() {
                $.alert('Failed to access because of network error.')
                });
            }
    })

    //Profile
    .controller('profileCtrl', function($scope, $rootScope, $http) {
        $scope.username = $rootScope.username;


        $http.post('http://' + $rootScope.hostUrl + ':8000/uiop/get-user-channel-list',
            JSON.stringify({
                username: $rootScope.username,
            })
        ).success(function (ret) {
            console.log(ret.channelList);
            $scope.channelList = ret.channelList;
        }).error(function() {
            $.alert('Failed to access because of network error.')
        });

        $scope.modifyUserPassword = function () {
            $http.post('http://' + $rootScope.hostUrl + ':8000/uiop/modify-user-password',
                JSON.stringify({
                    username: $rootScope.username,
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

    })



