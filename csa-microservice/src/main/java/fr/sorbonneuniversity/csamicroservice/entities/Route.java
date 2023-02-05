package fr.sorbonneuniversity.csamicroservice.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "route")
@AllArgsConstructor
@NoArgsConstructor
@Data
public class Route {
    @Id
    @Column(name = "route_id")
    public long routeId;

    @Column(name = "route_short_name")
    public String routeShortName;

    @Column(name = "route_type")
    public String routeType;

    @Column(name = "route_color")
    public String routeColor;
}
