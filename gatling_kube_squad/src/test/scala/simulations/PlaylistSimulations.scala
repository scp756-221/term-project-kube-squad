package simulations

import io.gatling.core.scenario.Simulation
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class PlaylistSimulations extends Simulation {

  val port = "6000"
  val host = "http://0.0.0.0"

  //  base_path_of_request_body
  val bp_rb = "./src/test/resources/bodies/playlist"

  // http conf
  val httpConf = http.baseUrl(s"$host:$port/api/v1/music/")
    .header("Accept", value="application/json")
    .header("content-type", value="application/json")


  // scenario
  val scn = scenario("Playlist CURD Scenario")
    .exec(
      http("get songs list")
        .get("getMusicList")
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("add song to playlist")
        .post("addToPlaylist")
        .body(RawFileBody(s"$bp_rb/AddToPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    //  http://0.0.0.0:6000/api/v1/music/


  .exec(
      http("view playlist names")
        .post("view_playlist_names")
        .body(RawFileBody(s"$bp_rb/ViewPlaylistNamesRequest.json")).asJson
        .check(status is 200)
    )


    .pause(3)

    .exec(
      http("view playlist")
        .post("view_playlist")
        .body(RawFileBody(s"$bp_rb/ViewPlaylistRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
        http("delete song from playlist")
          .post("delete_song_from_playlist")
          .body(RawFileBody(s"$bp_rb/DeleteSongFromPlaylist.json")).asJson
          .check(status is 200)
      )

  //  http://0.0.0.0:6000/api/v1/music/view_playlist
    setUp(scn.inject(atOnceUsers(1000))).protocols(httpConf)
}
