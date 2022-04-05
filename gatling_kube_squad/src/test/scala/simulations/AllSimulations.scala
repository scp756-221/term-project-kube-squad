package simulations

import io.gatling.core.Predef._
import io.gatling.core.scenario.Simulation
import io.gatling.http.Predef._


class AllSimulations extends Simulation {


//  ac2736187207c4a34861b48040bdfbcc-208095791.us-west-2.elb.amazonaws.com

  val port = "80"
  val host = "http://aefee6789db0e4e109bbc7410ed27da1-2098308503.us-west-2.elb.amazonaws.com"

  //  base_path_of_request_body
  val bp_rb = "./src/test/resources/bodies/auth"

  //  base_path_of_request_body
  val bp_rb1 = "./src/test/resources/bodies/playlist"


  //  base_path_of_request_body
  val bp_rb2 = "./src/test/resources/bodies/subcription"

  // http conf
  val httpConf = http.baseUrl(s"$host:$port")
    .header("Accept", value="application/json")
    .header("content-type", value="application/json")

  // scenario
  val scn = scenario("Auth Scenario")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
      )

      .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1 = scenario("Playlist CURD Scenario")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:6000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2 = scenario("Subscribe Module Scenario")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )



//  START of 2

  // scenario
  val scn_2 = scenario("Auth Scenario 2")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_2 = scenario("Playlist CURD Scenario 2")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:6000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_2 = scenario("Subscribe Module Scenario 2")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )




  //  START of 3

  // scenario
  val scn_3 = scenario("Auth Scenario 3")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_3 = scenario("Playlist CURD Scenario 3")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:6000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_3 = scenario("Subscribe Module Scenario 3")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )


  //  START of 4

  // scenario
  val scn_4 = scenario("Auth Scenario 4")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_4 = scenario("Playlist CURD Scenario 4")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:6000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_4 = scenario("Subscribe Module Scenario 4")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )



  //  START of 5

  // scenario
  val scn_5 = scenario("Auth Scenario 5")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_5 = scenario("Playlist CURD Scenario 5")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:6000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_5 = scenario("Subscribe Module Scenario 5")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )



  //  START of 6

  // scenario
  val scn_6 = scenario("Auth Scenario 6")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_6 = scenario("Playlist CURD Scenario 6")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:6000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_6 = scenario("Subscribe Module Scenario 6")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )


  //  START of 7

  // scenario
  val scn_7 = scenario("Auth Scenario 7")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_7 = scenario("Playlist CURD Scenario 7")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:7000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_7 = scenario("Subscribe Module Scenario 7")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )



  //  START of 8

  // scenario
  val scn_8 = scenario("Auth Scenario 8")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_8 = scenario("Playlist CURD Scenario 8")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:8000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_8 = scenario("Subscribe Module Scenario 8")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )


  //  START of 9

  // scenario
  val scn_9 = scenario("Auth Scenario 9")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_9 = scenario("Playlist CURD Scenario 9")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:9000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_9 = scenario("Subscribe Module Scenario 9")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )


  //  START of 10

  // scenario
  val scn_10 = scenario("Auth Scenario 10")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_10 = scenario("Playlist CURD Scenario 10")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:10000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_10 = scenario("Subscribe Module Scenario 10")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )


  //  START of 11

  // scenario
  val scn_11 = scenario("Auth Scenario 11")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_11 = scenario("Playlist CURD Scenario 11")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:11000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_11 = scenario("Subscribe Module Scenario 11")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )


  //  START of 12

  // scenario
  val scn_12 = scenario("Auth Scenario 12")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_12 = scenario("Playlist CURD Scenario 12")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:12000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_12 = scenario("Subscribe Module Scenario 12")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )


  //  START of 13

  // scenario
  val scn_13 = scenario("Auth Scenario 13")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_13 = scenario("Playlist CURD Scenario 13")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:13000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_13 = scenario("Subscribe Module Scenario 13")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )


  //  START of 14

  // scenario
  val scn_14 = scenario("Auth Scenario 14")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_14 = scenario("Playlist CURD Scenario 14")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:14000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_14 = scenario("Subscribe Module Scenario 14")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )


  //  START of 15

  // scenario
  val scn_15 = scenario("Auth Scenario 15")
    .exec(

      http("register user")
        .post("/api/v1/auth/register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("login user")
        .post("/api/v1/auth/login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("/api/v1/auth/logout")
        .check(status is 200)
    )



  // scenario
  val scn1_15 = scenario("Playlist CURD Scenario 15")
    .exec(
      http("get songs list")
        .get("/api/v1/music/getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("/api/v1/music/addToPlaylist")
        .body(RawFileBody(s"$bp_rb1/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:15000/api/v1/music/


    .exec(
      http("view playlist names")
        .post("/api/v1/music/view_playlist_names")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("/api/v1/music/view_playlist")
        .body(RawFileBody(s"$bp_rb1/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )




  // scenario
  val scn2_15 = scenario("Subscribe Module Scenario 15")
    .exec(
      http("Add Card")
        .post("/api/v1/subscribe/addcard")
        .body(RawFileBody(s"$bp_rb2/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Subcribe User")
        .post("/api/v1/subscribe/subcribe")
        .body(RawFileBody(s"$bp_rb2/SubcribeRequest.json")).asJson
        .check(status is 200)
    )


  // for loop execution with a range
    setUp(
      scn.inject(atOnceUsers(50)),
      scn1.inject(atOnceUsers(50)),
      scn2.inject(atOnceUsers(50)),


      scn_2.inject(atOnceUsers(50)),
      scn1_2.inject(atOnceUsers(50)),
      scn2_2.inject(atOnceUsers(50)),


      scn_3.inject(atOnceUsers(50)),
      scn1_3.inject(atOnceUsers(50)),
      scn2_3.inject(atOnceUsers(50)),


      scn_4.inject(atOnceUsers(50)),
      scn1_4.inject(atOnceUsers(50)),
      scn2_4.inject(atOnceUsers(50)),



      scn_5.inject(atOnceUsers(50)),
      scn1_5.inject(atOnceUsers(50)),
      scn2_5.inject(atOnceUsers(50)),


      scn_6.inject(atOnceUsers(50)),
      scn1_6.inject(atOnceUsers(50)),
      scn2_6.inject(atOnceUsers(50)),

      scn_7.inject(atOnceUsers(50)),
      scn1_7.inject(atOnceUsers(50)),
      scn2_7.inject(atOnceUsers(50)),


      scn_8.inject(atOnceUsers(50)),
      scn1_8.inject(atOnceUsers(50)),
      scn2_8.inject(atOnceUsers(50)),


      scn_9.inject(atOnceUsers(50)),
      scn1_9.inject(atOnceUsers(50)),
      scn2_9.inject(atOnceUsers(50)),


      scn_10.inject(atOnceUsers(50)),
      scn1_10.inject(atOnceUsers(50)),
      scn2_10.inject(atOnceUsers(50)),

      scn_11.inject(atOnceUsers(50)),
      scn1_11.inject(atOnceUsers(50)),
      scn2_11.inject(atOnceUsers(50)),

      scn_12.inject(atOnceUsers(50)),
      scn1_12.inject(atOnceUsers(50)),
      scn2_12.inject(atOnceUsers(50)),

      scn_13.inject(atOnceUsers(50)),
      scn1_13.inject(atOnceUsers(50)),
      scn2_13.inject(atOnceUsers(50)),

      scn_14.inject(atOnceUsers(50)),
      scn1_14.inject(atOnceUsers(50)),
      scn2_14.inject(atOnceUsers(50)),


      scn_15.inject(atOnceUsers(50)),
      scn1_15.inject(atOnceUsers(50)),
      scn2_15.inject(atOnceUsers(50)),
    ).protocols(httpConf)

}
