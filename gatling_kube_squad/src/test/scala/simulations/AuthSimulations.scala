package simulations

import io.gatling.core.Predef._
import io.gatling.core.scenario.Simulation
import io.gatling.http.Predef._


class AuthSimulations extends Simulation {

  val port = "5000"
  val host = "http://127.0.0.1"

  //  base_path_of_request_body
  val bp_rb = "./src/test/resources/bodies/auth"

  // http conf
  val httpConf = http.baseUrl(s"$host:$port/api/v1/auth/")
    .header("Accept", value="application/json")
    .header("content-type", value="application/json")

  // scenario
  val scn = scenario("Add User Scenario")
    .exec(

      http("register user")
        .post("register")
        .body(RawFileBody(s"$bp_rb/RegisterRequest.json")).asJson
        .check(status is 200)
      )

      .pause(3)

    .exec(
      http("login user")
        .post("login")
        .body(RawFileBody(s"$bp_rb/LoginRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
      http("logout user")
        .get("logout")
        .check(status is 200)
    )
  setUp(scn.inject(atOnceUsers(1000))).protocols(httpConf)

}
