package simulations

import io.gatling.core.scenario.Simulation
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class PremiumMusicInfoSimulations extends Simulation {

  val port = "6000"
  val host = "http://0.0.0.0"

  //  base_path_of_request_body
  val bp_rb = "./src/test/resources/bodies/playlist"

  // http conf
  val httpConf = http.baseUrl(s"$host:$port/api/v1/music/")
    .header("Accept", value="application/json")
    .header("content-type", value="application/json")

  val existing_song_id = "99"
  val missing_song_id = "1"
  val lyrics_info = "lyrics"
  val artist_info = "artist"
  val genre_info = "genre"
  val release_date_info = "release-date"
  val topic_info = "topic"

  //scenario

  val scn = scenario("Premium Music Info Scenario")
    //lyrics
    .exec(
      http("Lyrics/Existing song/Subscribed user")
        .get(existing_song_id+"/"+lyrics_info)
        .body(RawFileBody(s"$bp_rb/SubscribedUser.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Lyrics/Non-existent song/Subscribed user")
        .get(missing_song_id+"/"+lyrics_info)
        .body(RawFileBody(s"$bp_rb/SubscribedUser.json")).asJson
        .check(status is 404)
    )

    .pause(3)

    .exec(
      http("Lyrics/Existing song/Non-subscribed user")
        .get(existing_song_id+"/"+lyrics_info)
        .body(RawFileBody(s"$bp_rb/NonSubscribedUser.json")).asJson
        .check(status is 403)
    )

    .pause(3)

    .exec(
      http("Lyrics/Non-existent song/Non-subscribed user")
        .get(missing_song_id+"/"+lyrics_info)
        .body(RawFileBody(s"$bp_rb/NonSubscribedUser.json")).asJson
        .check(status is 403)
    )

    .pause(3)

    //artist
    .exec(
      http("Artist/Existing song/Subscribed user")
        .get(existing_song_id+"/"+artist_info)
        .body(RawFileBody(s"$bp_rb/SubscribedUser.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Artist/Non-existent song/Subscribed user")
        .get(missing_song_id+"/"+artist_info)
        .body(RawFileBody(s"$bp_rb/SubscribedUser.json")).asJson
        .check(status is 404)
    )

    .pause(3)

    .exec(
      http("Artist/Existing song/Non-subscribed user")
        .get(existing_song_id+"/"+artist_info)
        .body(RawFileBody(s"$bp_rb/NonSubscribedUser.json")).asJson
        .check(status is 403)
    )

    .pause(3)

    .exec(
      http("Artist/Non-existent song/Non-subscribed user")
        .get(missing_song_id+"/"+artist_info)
        .body(RawFileBody(s"$bp_rb/NonSubscribedUser.json")).asJson
        .check(status is 403)
    )

    .pause(3)

    //genre
    .exec(
      http("Genre/Existing song/Subscribed user")
        .get(existing_song_id+"/"+genre_info)
        .body(RawFileBody(s"$bp_rb/SubscribedUser.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Genre/Non-existent song/Subscribed user")
        .get(missing_song_id+"/"+genre_info)
        .body(RawFileBody(s"$bp_rb/SubscribedUser.json")).asJson
        .check(status is 404)
    )

    .pause(3)

    .exec(
      http("Genre/Existing song/Non-subscribed user")
        .get(existing_song_id+"/"+genre_info)
        .body(RawFileBody(s"$bp_rb/NonSubscribedUser.json")).asJson
        .check(status is 403)
    )

    .pause(3)

    .exec(
      http("Genre/Non-existent song/Non-subscribed user")
        .get(missing_song_id+"/"+genre_info)
        .body(RawFileBody(s"$bp_rb/NonSubscribedUser.json")).asJson
        .check(status is 403)
    )

    .pause(3)

    //release-date
    .exec(
      http("Release-Date/Existing song/Subscribed user")
        .get(existing_song_id+"/"+release_date_info)
        .body(RawFileBody(s"$bp_rb/SubscribedUser.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Release-Date/Non-existent song/Subscribed user")
        .get(missing_song_id+"/"+release_date_info)
        .body(RawFileBody(s"$bp_rb/SubscribedUser.json")).asJson
        .check(status is 404)
    )

    .pause(3)

    .exec(
      http("Release-Date/Existing song/Non-subscribed user")
        .get(existing_song_id+"/"+release_date_info)
        .body(RawFileBody(s"$bp_rb/NonSubscribedUser.json")).asJson
        .check(status is 403)
    )

    .pause(3)

    .exec(
      http("Release-Date/Non-existent song/Non-subscribed user")
        .get(missing_song_id+"/"+release_date_info)
        .body(RawFileBody(s"$bp_rb/NonSubscribedUser.json")).asJson
        .check(status is 403)
    )

    .pause(3)

    //topic
    .exec(
      http("Topic/Existing song/Subscribed user")
        .get(existing_song_id+"/"+topic_info)
        .body(RawFileBody(s"$bp_rb/SubscribedUser.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("Topic/Non-existent song/Subscribed user")
        .get(missing_song_id+"/"+topic_info)
        .body(RawFileBody(s"$bp_rb/SubscribedUser.json")).asJson
        .check(status is 404)
    )

    .pause(3)

    .exec(
      http("Topic/Existing song/Non-subscribed user")
        .get(existing_song_id+"/"+topic_info)
        .body(RawFileBody(s"$bp_rb/NonSubscribedUser.json")).asJson
        .check(status is 403)
    )

    .pause(3)

    .exec(
      http("Topic/Non-existent song/Non-subscribed user")
        .get(missing_song_id+"/"+topic_info)
        .body(RawFileBody(s"$bp_rb/NonSubscribedUser.json")).asJson
        .check(status is 403)
    )


    setUp(scn.inject(atOnceUsers(750))).protocols(httpConf)
}
