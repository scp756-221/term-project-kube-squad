package simulations

import io.gatling.core.Predef._
import io.gatling.core.scenario.Simulation
import io.gatling.http.Predef._


class SubscriptionSimulations extends Simulation {

  val port = "4000"
  val host = "http://0.0.0.0"

  //  base_path_of_request_body
  val bp_rb = "./src/test/resources/bodies/subcription"

  // http conf
  val httpConf = http.baseUrl(s"$host:$port/api/v1/subscribe/")
    .header("Accept", value="application/json")
    .header("content-type", value="application/json")

  // scenario
  val scn = scenario("Subcribe Module Scenario")
    .exec(
      http("Add Card")
        .post("addcard")
        .body(RawFileBody(s"$bp_rb/AddCardRequest.json")).asJson
        .check(status is 200)
    )

    .pause(3)

    .exec(
          http("Subcribe User")
            .post("subcribe")
            .body(RawFileBody(s"$bp_rb/SubcribeRequest.json")).asJson
            .check(status is 200)
    )
  setUp(scn.inject(atOnceUsers(1000))).protocols(httpConf)
}
