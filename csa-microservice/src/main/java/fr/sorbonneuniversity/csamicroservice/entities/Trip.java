package fr.sorbonneuniversity.csamicroservice.entities;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Entity
@Table(name = "stop")
@AllArgsConstructor
@NoArgsConstructor
@Data
public class Trip {
    @Id
    @Column(name = "trip_id")
    public long tripId;

    @OneToMany
    public List<Route> routes;
}
