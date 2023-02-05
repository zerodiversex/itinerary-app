package fr.sorbonneuniversity.stopsmicroservice.repositories;

import fr.sorbonneuniversity.stopsmicroservice.entities.Stop;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface StopRepository extends JpaRepository<Stop, Long> {
    List<Stop> findAllByStopNameContaining(String name);
}
