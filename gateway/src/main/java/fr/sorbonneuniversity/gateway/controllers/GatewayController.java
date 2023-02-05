package fr.sorbonneuniversity.gateway.controllers;

import fr.sorbonneuniversity.gateway.entities.Stop;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/v1")
@AllArgsConstructor
@CrossOrigin(value = "*")
public class GatewayController {

    private RestTemplate restTemplate;

    @GetMapping(value = {"/stops", "/stops/"})
    public ResponseEntity<List<Stop>> getAllStops(@RequestParam(required = false, name = "ids") List<Long> ids, @RequestParam(required = false, name = "search") String name) {

        Stop[] stop = restTemplate.getForObject(
                "http://localhost:8081/api/v1/stops", Stop[].class);

        return ResponseEntity.ok().body(Arrays.stream(stop).collect(Collectors.toList()));
    }

    @GetMapping(value = {"/csa", "/csa/"})
    public ResponseEntity<List<Stop>> getCSAResult(@RequestParam(required = false, name = "ids") List<Long> ids, @RequestParam(required = false, name = "search") String name) {

        Stop[] stop = restTemplate.getForObject(
                "http://localhost:8082/api/v1/result", Stop[].class);

        return ResponseEntity.ok().body(Arrays.stream(stop).collect(Collectors.toList()));
    }

    @GetMapping(value = {"/raptor", "/raptor/"})
    public ResponseEntity<List<Stop>> getRaptorResult(@RequestParam(required = false, name = "ids") List<Long> ids, @RequestParam(required = false, name = "search") String name) {

        Stop[] stop = restTemplate.getForObject(
                "http://localhost:8083/api/v1/result", Stop[].class);

        return ResponseEntity.ok().body(Arrays.stream(stop).collect(Collectors.toList()));
    }
}
