package fr.sorbonneuniversity.stopsmicroservice.services;

import fr.sorbonneuniversity.stopsmicroservice.entities.Stop;
import fr.sorbonneuniversity.stopsmicroservice.repositories.StopRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@AllArgsConstructor
public class StopService {
    private final StopRepository stopRepository;

    public List<Stop> getAllStops() {
        return stopRepository.findAll();
    }

    public List<Stop> searchStopsByName(String name) {
        return stopRepository.findAllByStopNameContaining(name);
    }


    public List<Stop> getStopsByIds(List<Long> ids) {
        return stopRepository.findAllById(ids);
    }

    public Stop getStopById(Long stopId) {
        return stopRepository.findById(stopId).orElse(null);
    }
}
