/**
 * Created by ShellyXia on 18/3/25.
 */
var myApp = angular.module('myApp', ['ui.router', 'myApp.controllers', 'monospaced.qrcode']);

var isLogin = false;
var notLogin = true;
var enter_Channel = false;

myApp.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider ) {

    $urlRouterProvider.when('', '/home');
    $stateProvider
        //home
        .state('home', {
            url:'/home',
            cache:'false',
            templateUrl: 'templates/home.html',
            controller: 'homeCtrl'
        })

        //Channel
        .state('channel', {
            url: '/channel/:channel_code',
            cache: 'false',
            templateUrl: 'templates/channel.html',
            controller: 'channelCtrl'
        })

        //EnterPassword
        .state('enterPassword', {
            url: '/enterPassword/:channel_code',
            cache: 'false',
            templateUrl: 'templates/enterChannelPassword.html',
            controller: 'enterChannelPasswordCtrl'
        })

        //Login
        .state('login', {
            url: '/login',
            templateUrl: 'templates/login.html',
            controller: 'loginCtrl'
        })

        //Signup
        .state('signup', {
            url: '/signup',
            templateUrl: 'templates/signup.html',
            controller: 'signupCtrl'
        })

        //Profile
        .state('profile', {
            url:'/profile',
            cache:'false',
            templateUrl: 'templates/profile.html',
            controller: 'profileCtrl'
        })
}]);

myApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}).config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post = {"Content-Type": "application/json"}
}]);