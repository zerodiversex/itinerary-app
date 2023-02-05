package fr.sorbonneuniversity.stopsmicroservice.controllers;

import fr.sorbonneuniversity.stopsmicroservice.entities.Stop;
import fr.sorbonneuniversity.stopsmicroservice.services.StopService;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/stops")
@AllArgsConstructor
@CrossOrigin(value = "*")
public class StopController {
    private final StopService stopService;

    @GetMapping(value = {"", "/"})
    public ResponseEntity<List<Stop>> getAllStops(@RequestParam(required = false, name = "ids") List<Long> ids, @RequestParam(required = false, name = "search") String name) {

        if (name != null) {
            return ResponseEntity.ok().body(stopService.searchStopsByName(name));
        }

        if (ids != null && ids.size() > 0) {
            return ResponseEntity.ok().body(stopService.getStopsByIds(ids));
        }

        return ResponseEntity.ok().body(stopService.getAllStops());
    }

    @GetMapping(value = {"/{stopId}", "/{stopId}/"})
    public ResponseEntity<Stop> getAllStops(@PathVariable Long stopId) {
        return ResponseEntity.ok().body(stopService.getStopById(stopId));
    }
}
