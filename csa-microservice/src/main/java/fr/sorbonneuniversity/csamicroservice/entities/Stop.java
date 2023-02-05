package fr.sorbonneuniversity.csamicroservice.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "stop")
@AllArgsConstructor
@NoArgsConstructor
@Data
public class Stop {
    @Id
    @Column(name = "stop_id")
    public long stopId;

    @Column(name = "stop_name")
    public String stopName;

    @Column(name = "stop_desc")
    public String stopDesc;

    @Column(name = "stop_lat")
    public String stopLat;

    @Column(name = "stop_lon")
    public String stopLon;
}
